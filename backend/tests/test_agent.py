"""The supervisor and SQL sub-agent wiring, driven by scripted models (no LLM, no database)."""

import psycopg
import pytest
from helpers import BrokenModel, scripted, tool_call
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

from app.agent.assistant import (
    FALLBACK_REPLY,
    HIDDEN_FLAG,
    LOOKUP_TOOL,
    AssistantUnavailable,
    CourierAssistant,
    build_assistant_graph,
    final_reply,
)
from app.agent.context import CourierContext
from app.agent.sql_agent import MAX_QUERIES, build_sql_agent
from app.database import QueryResult
from app.security import ChatSession

CUSTOMER = CourierContext(mode="customer", user_id=1, display_name="Habib")


class FakeSandbox:
    def __init__(self, rows=None, error=None):
        self.calls = []
        self.rows = rows if rows is not None else [{"n": 18}]
        self.error = error

    async def run_scoped(self, sql, scope):
        self.calls.append((sql, scope))
        if self.error:
            raise self.error
        return QueryResult(
            columns=list(self.rows[0]) if self.rows else [], rows=self.rows, truncated=False
        )


def make_assistant(supervisor_replies, sql_agent, **kwargs):
    graph = build_assistant_graph(
        scripted(supervisor_replies),
        sql_agent,
        InMemorySaver(),
        summary_trigger_tokens=kwargs.pop("summary_trigger_tokens", 4000),
        summary_keep_messages=kwargs.pop("summary_keep_messages", 20),
        **kwargs,
    )
    return CourierAssistant(graph), graph


async def thread_messages(graph, thread_id):
    state = await graph.aget_state({"configurable": {"thread_id": thread_id}})
    return state.values["messages"]


async def run_sql_agent(sql_replies, sandbox):
    agent = build_sql_agent(scripted(sql_replies), sandbox, max_rows=50)
    result = await agent.ainvoke({"messages": [HumanMessage("question")]}, context=CUSTOMER)
    return [m for m in result["messages"] if isinstance(m, ToolMessage)]


async def test_data_questions_reach_the_sandbox_with_the_server_scope():
    sandbox = FakeSandbox()
    sql_agent = build_sql_agent(
        scripted(
            [
                tool_call("run_sql", query="select count(*) as n from shipments"),
                AIMessage("The customer has 18 shipments."),
            ]
        ),
        sandbox,
        max_rows=50,
    )
    assistant, graph = make_assistant(
        [
            tool_call(LOOKUP_TOOL, question="How many shipments do I have?"),
            AIMessage("You have **18** shipments."),
        ],
        sql_agent,
    )
    reply = await assistant.reply(ChatSession("t1", CUSTOMER), "how many shipments?")

    assert reply == "You have **18** shipments."
    assert sandbox.calls == [("SELECT COUNT(*) AS n FROM shipments LIMIT 51", CUSTOMER)]
    tool_result = next(m for m in await thread_messages(graph, "t1") if isinstance(m, ToolMessage))
    assert tool_result.content == "The customer has 18 shipments."


async def test_unsafe_sql_never_reaches_the_database():
    sandbox = FakeSandbox()
    results = await run_sql_agent(
        [tool_call("run_sql", query="DROP TABLE shipments"), AIMessage("I can't do that.")], sandbox
    )
    assert sandbox.calls == []
    assert results[0].content.startswith("Query rejected:")


async def test_database_errors_go_back_to_the_sub_agent():
    sandbox = FakeSandbox(error=psycopg.errors.UndefinedColumn('column "eta" does not exist'))
    results = await run_sql_agent(
        [tool_call("run_sql", query="SELECT eta FROM shipments"), AIMessage("No ETA column.")],
        sandbox,
    )
    assert results[0].content == 'Database error: column "eta" does not exist'


async def test_the_sub_agent_gets_a_limited_number_of_queries():
    sandbox = FakeSandbox()
    attempts = [tool_call("run_sql", query="SELECT 1 AS n") for _ in range(MAX_QUERIES + 1)]
    results = await run_sql_agent([*attempts, AIMessage("Done.")], sandbox)
    assert len(sandbox.calls) == MAX_QUERIES
    assert "limit" in results[-1].content.lower()


async def test_a_failing_lookup_still_lets_the_assistant_answer():
    class BrokenSubAgent:
        async def ainvoke(self, *args, **kwargs):
            raise RuntimeError("database down")

    assistant, graph = make_assistant(
        [
            tool_call(LOOKUP_TOOL, question="Where is TN1?"),
            AIMessage("The records are unavailable right now, please try again shortly."),
        ],
        BrokenSubAgent(),
    )
    reply = await assistant.reply(ChatSession("t2", CUSTOMER), "where is my package?")
    assert "unavailable" in reply
    tool_result = next(m for m in await thread_messages(graph, "t2") if isinstance(m, ToolMessage))
    assert tool_result.content.startswith("The lookup failed.")


async def test_a_model_outage_raises_assistant_unavailable():
    graph = build_assistant_graph(
        BrokenModel(messages=iter([])),
        None,
        InMemorySaver(),
        summary_trigger_tokens=4000,
        summary_keep_messages=20,
    )
    with pytest.raises(AssistantUnavailable):
        await CourierAssistant(graph).reply(ChatSession("t3", CUSTOMER), "hello")


async def test_long_threads_are_summarized_past_the_threshold():
    long_answer = "Your shipment TN4255-8215-9617 left Tunis and is on its way to Lyon. " * 4
    summary_model = scripted(
        [AIMessage("- Customer Habib asked about TN4255-8215-9617 (Tunis to Lyon).")]
    )
    assistant, graph = make_assistant(
        [AIMessage(long_answer), AIMessage(long_answer), AIMessage("Anything else?")],
        None,
        summary_model=summary_model,
        summary_trigger_tokens=120,
        summary_keep_messages=2,
    )
    session = ChatSession("t4", CUSTOMER)
    for question in ("Where is my package?", "And where was it before?", "Thanks!"):
        await assistant.reply(session, question)

    messages = await thread_messages(graph, "t4")
    summaries = [m for m in messages if m.additional_kwargs.get("lc_source") == "summarization"]
    assert summaries and "TN4255-8215-9617" in summaries[0].text
    assert len(messages) < 6  # older turns were replaced by the summary


async def test_hidden_turns_are_flagged_in_the_thread():
    assistant, graph = make_assistant([AIMessage("It is in transit.")], None)
    await assistant.reply(ChatSession("t5", CUSTOMER), "Give updates", hidden=True)
    first = (await thread_messages(graph, "t5"))[0]
    assert isinstance(first, HumanMessage) and first.additional_kwargs[HIDDEN_FLAG] is True


def test_final_reply_ignores_tool_calls_and_has_a_fallback():
    assert (
        final_reply([AIMessage("Here you go."), tool_call(LOOKUP_TOOL, question="q")])
        == "Here you go."
    )
    assert final_reply([HumanMessage("hi")]) == FALLBACK_REPLY

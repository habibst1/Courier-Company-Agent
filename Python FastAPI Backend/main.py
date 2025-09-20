# main.py
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any, Optional
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from sqlalchemy import create_engine, text
from models import QueryRequest, QueryResponse
from pydantic import BaseModel

# DB Setup
DB_URI = "postgresql://postgres:bonbon2003@localhost:5432/courier_db"
engine = create_engine(DB_URI)

SCHEMA_INFO = """
TABLE 1 (users): id, username, email, full_name, phone, created_at
TABLE 2 (addresses): id, user_id, address_line, city, state, country, postal_code, created_at
TABLE 3 (shipments): id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date
TABLE 4 (tracking_updates): id, shipment_id, status, location_city, location_details, scanned_at, created_by

Indexes:
- shipments(user_id)
- shipments(tracking_number)
- tracking_updates(shipment_id, scanned_at DESC)
"""

# LLM Setup
os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    temperature=0.4,
    model_name="openai/gpt-oss-20b",
)

class ConversationHistory:
    def __init__(self, history_type: str):
        self.history = []
        self.history_type = history_type
        print(f"🆕 ConversationHistory initialized for {history_type}")
    
    def add_entry(self, user_question: str, ai_response: str, response_type: str):
        entry = {
            "user_question": user_question,
            "ai_response": ai_response,
            "response_type": response_type,
        }
        self.history.append(entry)
        print(f"📝 Added to {self.history_type} conversation history: {entry}")
    
    def get_history(self) -> List[Dict]:
        print(f"📋 Retrieving full {self.history_type} conversation history ({len(self.history)} entries)")
        return self.history
    
    def get_formatted_history(self) -> str:
        formatted = ""
        for entry in self.history[-10:]:  # Last 10 conversations
            formatted += f"User: {entry['user_question']}\nAI: {entry['ai_response']}\n\n"
        print(f"📖 Formatted {self.history_type} history (last {min(10, len(self.history))} entries):\n{formatted}")
        return formatted

class OrchestratorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.memory = ConversationBufferMemory(memory_key="history")
        
        # Separate conversation histories for each use case
        self.authenticated_history = ConversationHistory("authenticated_users")
        self.anonymous_history = ConversationHistory("anonymous_users")
        
        print("🆕 OrchestratorAgent initialized")
        
        # Prompt for authenticated users (with user_id)
        self.authenticated_prompt = PromptTemplate(
            input_variables=["question", "user_id", "conversation_history"],
            template="""You are a courier service assistant for authenticated users. You can answer general questions about shipping and courier services, or get specific data about the user's shipments using an SQL agent.

Available context:
- User ID: {user_id}

Conversation History:
{conversation_history}

User Question: {question}

Instructions:
- If it's a general question about shipping, delivery, policies, or how things work - answer directly
- If they need specific data about their shipments (track packages, show orders, check statuses, etc.) - respond: "SQL_NEEDED: [simple question]"
- If you have response from conversation history , no need to sql and answer with what you know

Examples:
- "How long does shipping take?" → Answer directly
- "Show my orders" → "SQL_NEEDED: get orders for user {user_id}"
- "What's the status of my recent shipments?" → "SQL_NEEDED: get recent shipments for user {user_id}"

Response:"""
        )
        
        # Prompt for anonymous users (with tracking number)
        self.anonymous_prompt = PromptTemplate(
            input_variables=["question", "tracking_number", "conversation_history"],
            template="""You are a courier service assistant for package recipients. You can answer general questions about shipping and courier services, or get specific data about a tracked package using an SQL agent.

Available context:
- Tracking Number: {tracking_number}

Conversation History:
{conversation_history}

User Question: {question}

Instructions:
- If it's a general question about shipping, delivery, policies, or how things work - answer directly
- If they need specific data about a tracked package (details , status, location, delivery date, etc.) - respond: "SQL_NEEDED: [simple question]"

Examples:
- "How long does shipping take?" → Answer directly
- "Where is my package with tracking ABC123?" → "SQL_NEEDED: get status of tracking ABC123"
- "When will package XYZ456 be delivered?" → "SQL_NEEDED: get delivery date for tracking XYZ456"

Response:"""
        )
        
        self.authenticated_chain = LLMChain(llm=self.llm, prompt=self.authenticated_prompt)
        self.anonymous_chain = LLMChain(llm=self.llm, prompt=self.anonymous_prompt)
        print("🔗 LLMChains created for OrchestratorAgent")
    
    def process(self, question: str, user_id: Optional[int], tracking_number: Optional[str]) -> Dict[str, Any]:
        print(f"\n{'='*60}")
        print("🎭 ORCHESTRATOR AGENT PROCESSING")
        print(f"📥 Input - Question: '{question}', User ID: {user_id}, Tracking: {tracking_number}")
        
        # Determine which use case we're handling
        if user_id:
            print("👤 Authenticated user detected")
            history = self.authenticated_history
            chain = self.authenticated_chain
            prompt_vars = {
                "question": question,
                "user_id": user_id,
                "conversation_history": history.get_formatted_history()
            }
        elif tracking_number:
            print("👥 Anonymous user (tracking) detected")
            history = self.anonymous_history
            chain = self.anonymous_chain
            prompt_vars = {
                "question": question,
                "tracking_number": tracking_number,
                "conversation_history": history.get_formatted_history()
            }
        else:
            print("❓ No user_id or tracking_number provided - using authenticated flow as fallback")
            history = self.authenticated_history
            chain = self.authenticated_chain
            prompt_vars = {
                "question": question,
                "user_id": "None",
                "conversation_history": history.get_formatted_history()
            }
        
        print(f"📋 Prompt variables: {prompt_vars}")
        
        # Get the formatted prompt
        formatted_prompt = chain.prompt.format(**prompt_vars)
        print(f"📄 Formatted prompt sent to LLM:\n{formatted_prompt}")
        print("-" * 40)
        
        response = chain.run(**prompt_vars)
        
        print(f"📤 LLM Response: '{response}'")
        
        self.memory.chat_memory.add_user_message(question)
        print(f"💾 Added user message to memory: '{question}'")
        
        if response.startswith("SQL_NEEDED:"):
            refined_question = response.replace("SQL_NEEDED:", "").strip()
            print(f"🔍 SQL needed detected. Refined question: '{refined_question}'")
            return {"type": "sql_needed", "refined_question": refined_question}
        else:
            self.memory.chat_memory.add_ai_message(response)
            print(f"💾 Added AI message to memory: '{response}'")
            # Store in appropriate conversation history
            history.add_entry(question, response, "general")
            return {"type": "general", "response": response}
    
    def add_sql_response_to_history(self, user_question: str, sql_response: str, user_id: Optional[int], tracking_number: Optional[str]):
        """Add SQL agent response to appropriate conversation history"""
        if user_id:
            print(f"💾 Adding SQL response to authenticated history for question: '{user_question}'")
            self.authenticated_history.add_entry(user_question, sql_response, "sql")
        elif tracking_number:
            print(f"💾 Adding SQL response to anonymous history for question: '{user_question}'")
            self.anonymous_history.add_entry(user_question, sql_response, "sql")
        else:
            print(f"💾 Adding SQL response to authenticated history (fallback) for question: '{user_question}'")
            self.authenticated_history.add_entry(user_question, sql_response, "sql")

class SQLAgent:
    def __init__(self, db_engine, schema_info, llm):
        self.db_engine = db_engine
        self.schema_info = schema_info
        self.llm = llm
        print("🆕 SQLAgent initialized")
        
        self.sql_prompt = PromptTemplate(
            input_variables=["question", "schema"],
            template="""Generate a PostgreSQL query for this request.

Request: {question}
            
Database Schema:
{schema}

Important Guidelines:
1. Only query tables mentioned in the schema
2. If you need more informations, respond with "NEED_MORE_INFO: [your question]"
3. Use proper JOINs when needed
4. Order results by newest first unless specified otherwise
5. Limit results to 10 records unless specified otherwise


Return ONLY a VALID SQL query directly without any explanations or quotes or ```sql

SQL Query:"""
        )
        
        self.response_prompt = PromptTemplate(
            input_variables=["original_question", "data"],
            template="""Answer the user's question based on this data:

Question: {original_question}
Data: {data}

Give a helpful, natural response. If no data, say so politely.

-If the question is asking about informations about a tracking shipment , do not return ids , just return basic informations.
-If you found error on data , just respond "We have internal problems, ask again later."

Response:"""
        )
        
        self.sql_chain = LLMChain(llm=self.llm, prompt=self.sql_prompt)
        self.response_chain = LLMChain(llm=self.llm, prompt=self.response_prompt)
        print("🔗 LLMChains created for SQLAgent")
    
    def execute_query(self, query: str) -> List[Dict]:
        print(f"🗄️ Executing SQL query: {query}")
        try:
            with self.db_engine.connect() as connection:
                result = connection.execute(text(query))
                columns = result.keys()
                results = [dict(zip(columns, row)) for row in result.fetchall()]
                print(f"✅ Query executed successfully. Results: {results}")
                return results
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Query execution failed: {error_msg}")
            return [{"error": error_msg}]
    
    def process(self, refined_question: str, original_question: str) -> Dict[str, Any]:
        print(f"\n{'='*60}")
        print("🗄️ SQL AGENT PROCESSING")
        print(f"📥 Input - Refined question: '{refined_question}', Original: '{original_question}'")
        
        # Generate SQL query
        sql_prompt_vars = {
            "question": refined_question,
            "schema": self.schema_info
        }
        
        formatted_sql_prompt = self.sql_prompt.format(**sql_prompt_vars)
        print(f"📄 SQL prompt sent to LLM:\n{formatted_sql_prompt}")
        print("-" * 40)
        
        sql_response = self.sql_chain.run(**sql_prompt_vars)
        print(f"📤 SQL LLM Response: '{sql_response}'")
        
        if sql_response.startswith("NEED_MORE_INFO:"):
            info_needed = sql_response.replace("NEED_MORE_INFO:", "").strip()
            print(f"❓ Need more info: {info_needed}")
            return {"type": "clarification", "message": info_needed}
        
        # Execute the query
        results = self.execute_query(sql_response)
        
        # Generate natural language response
        response_prompt_vars = {
            "original_question": original_question,
            "data": str(results)
        }
        
        formatted_response_prompt = self.response_prompt.format(**response_prompt_vars)
        print(f"📄 Response prompt sent to LLM:\n{formatted_response_prompt}")
        print("-" * 40)
        
        natural_response = self.response_chain.run(**response_prompt_vars)
        print(f"📤 Response LLM Response: '{natural_response}'")
        
        result = {
            "type": "results",
            "query": sql_response,
            "data": results,
            "response": natural_response
        }
        
        print(f"✅ SQL Agent processing complete. Result type: {result['type']}")
        return result

class CourierService:
    def __init__(self, db_engine, schema_info, llm):
        self.orchestrator = OrchestratorAgent(llm)
        self.sql_agent = SQLAgent(db_engine, schema_info, llm)
        print("🆕 CourierService initialized")
    
    def process_query(self, question: str, user_id: Optional[int] = None, tracking_number: Optional[str] = None) -> Dict[str, Any]:
        print(f"\n{'='*60}")
        print("🚀 COURIER SERVICE PROCESSING QUERY")
        print(f"📥 Input - Question: '{question}', User ID: {user_id}, Tracking: {tracking_number}")
        
        # First, let orchestrator handle it
        result = self.orchestrator.process(question, user_id, tracking_number)
        print(f"🎭 Orchestrator result type: {result['type']}")
        
        if result["type"] == "sql_needed":
            print("🔄 Passing to SQL Agent...")
            # Pass to SQL agent
            sql_result = self.sql_agent.process(result["refined_question"], question)
            
            # Add SQL response to appropriate conversation history
            if sql_result["type"] == "results":
                self.orchestrator.add_sql_response_to_history(
                    question, 
                    sql_result["response"], 
                    user_id, 
                    tracking_number
                )
            
            print(f"✅ Final result from SQL Agent: {sql_result['type']}")
            return sql_result
        else:
            print(f"✅ Final result from Orchestrator: {result['type']}")
            return result
    
    def get_conversation_history(self, history_type: str = "authenticated") -> List[Dict]:
        """Get the conversation history for a specific use case"""
        print(f"📋 Retrieving {history_type} conversation history")
        if history_type == "anonymous":
            return self.orchestrator.anonymous_history.get_history()
        else:
            return self.orchestrator.authenticated_history.get_history()

# Initialize service
print("🔧 Initializing CourierService...")
courier_service = CourierService(engine, SCHEMA_INFO, llm)
print("✅ Service initialization complete!")

# FastAPI App
app = FastAPI(title="Courier API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    print(f"\n{'='*60}")
    print("🌐 API REQUEST RECEIVED")
    print(f"📥 Request: {request.dict()}")
    
    result = courier_service.process_query(
        question=request.question,
        user_id=request.user_id,
        tracking_number=request.tracking_number
    )
    
    print(f"📤 API Response: {result}")
    print(f"{'='*60}\n")
    return result

@app.get("/conversation-history")
async def get_conversation_history(history_type: str = "authenticated"):
    """Endpoint to retrieve conversation history for a specific use case"""
    print(f"🌐 {history_type} conversation history API request")
    return courier_service.get_conversation_history(history_type)

@app.get("/health")
async def health_check():
    print("🌐 Health check API request")
    return {"status": "ok"}


if __name__ == "__main__":
    print("🚀 Starting FastAPI server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
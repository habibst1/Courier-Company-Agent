"""HTTP behaviour with the database and the assistant replaced by fakes."""

import json

import pytest
from helpers import offline_settings
from httpx import ASGITransport, AsyncClient

from app.agent.assistant import AssistantUnavailable
from app.main import create_app
from app.security import Customer, LoginTokens, SessionTokens, hash_password
from app.services import Services

TRACKED = "TN4255-8215-9617"
PASSWORD = "correct horse battery staple"
PROFILE = {
    "username": "habib_bencheikhali",
    "full_name": "Habib BEN CHEIKH ALI",
    "email": "habib.bencheikh@email.com",
    "phone": "+21624123456",
}
LOGIN_ROW = {
    "user_id": 1,
    "username": "habib_bencheikhali",
    "full_name": "Habib BEN CHEIKH ALI",
    "password_hash": hash_password(PASSWORD),
}


class FakeDB:
    async def ping(self):
        return True

    async def tracking_number_exists(self, tracking_number):
        return tracking_number == TRACKED

    async def customer_profile(self, user_id):
        return PROFILE if user_id == 1 else None

    async def find_login(self, identifier):
        return LOGIN_ROW if identifier.lower() in {"habib_bencheikhali", PROFILE["email"]} else None


class FakeAssistant:
    def __init__(self):
        self.calls = []
        self.error = None
        self.turns = [{"role": "assistant", "content": "It is in transit to Lyon."}]

    async def reply(self, session, text, *, hidden=False):
        self.calls.append((session, text, hidden))
        if self.error:
            raise self.error
        return "It is in transit to Lyon."

    async def stream(self, session, text, *, hidden=False):
        self.calls.append((session, text, hidden))
        yield "status", "Checking the shipment records…"
        if self.error:
            raise self.error
        for token in ("It is ", "in transit."):
            yield "token", token
        yield "done", "It is in transit."

    async def history(self, session):
        self.calls.append((session, None, None))
        return self.turns, True


@pytest.fixture
def services():
    settings = offline_settings()
    secret = settings.session_secret.get_secret_value()
    return Services(
        settings=settings,
        db=FakeDB(),
        tokens=SessionTokens(secret, 1),
        logins=LoginTokens(secret, 1),
        assistant=FakeAssistant(),
    )


@pytest.fixture
async def client(services):
    app = create_app(services=services)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
        yield http


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


async def start_recipient_chat(client):
    response = await client.post(
        "/api/sessions", json={"mode": "recipient", "tracking_number": TRACKED}
    )
    return response.json()["session_token"]


async def sign_in(client, username="habib_bencheikhali", password=PASSWORD):
    return await client.post("/api/auth/login", json={"username": username, "password": password})


async def test_health(client):
    assert (await client.get("/api/health")).json() == {"status": "ok", "database": True}


async def test_recipient_session_normalizes_and_scopes_the_tracking_number(client, services):
    response = await client.post(
        "/api/sessions", json={"mode": "recipient", "tracking_number": " tn4255-8215-9617 "}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["tracking_number"] == TRACKED and body["customer"] is None
    session = services.tokens.read(body["session_token"])
    assert session.context.mode == "recipient" and session.context.tracking_number == TRACKED


@pytest.mark.parametrize(
    ("payload", "status"),
    [
        ({"mode": "recipient", "tracking_number": "TN0000-0000-0000"}, 404),
        ({"mode": "recipient", "tracking_number": "x' OR 1=1 --"}, 422),
        ({"mode": "recipient"}, 422),
        ({"mode": "admin"}, 422),
    ],
)
async def test_bad_session_requests(client, payload, status):
    assert (await client.post("/api/sessions", json=payload)).status_code == status


@pytest.mark.parametrize("username", ["habib_bencheikhali", "HABIB.BENCHEIKH@email.com"])
async def test_sign_in_with_user_name_or_email(client, services, username):
    response = await sign_in(client, username)
    assert response.status_code == 200
    body = response.json()
    assert body["user"] == {"username": "habib_bencheikhali", "full_name": "Habib BEN CHEIKH ALI"}
    assert services.logins.read(body["access_token"]).user_id == 1


@pytest.mark.parametrize(
    ("username", "password"), [("habib_bencheikhali", "wrong"), ("nobody", PASSWORD)]
)
async def test_failed_sign_in_does_not_say_which_part_was_wrong(client, username, password):
    response = await sign_in(client, username, password)
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong user name or password."


async def test_customer_chats_need_a_sign_in(client, services):
    assert (await client.post("/api/sessions", json={"mode": "customer"})).status_code == 401
    chat_token = await start_recipient_chat(client)
    # A chat-session token can't stand in for a login token.
    as_login = await client.post(
        "/api/sessions", json={"mode": "customer"}, headers=bearer(chat_token)
    )
    assert as_login.status_code == 401
    gone = services.logins.issue(Customer(user_id=999, username="gone", full_name=None))
    deleted = await client.post("/api/sessions", json={"mode": "customer"}, headers=bearer(gone))
    assert deleted.status_code == 401


async def test_customer_session_is_scoped_to_the_signed_in_customer(client, services):
    login = (await sign_in(client)).json()
    response = await client.post(
        "/api/sessions",
        json={"mode": "customer", "user_id": 2},  # ignored: the login decides
        headers=bearer(login["access_token"]),
    )
    body = response.json()
    assert body["customer"] == PROFILE
    context = services.tokens.read(body["session_token"]).context
    assert (context.mode, context.user_id, context.display_name) == (
        "customer",
        1,
        "Habib BEN CHEIKH ALI",
    )


async def test_chat_requires_a_valid_session(client):
    assert (await client.post("/api/chat", json={"message": "hi"})).status_code == 401
    forged = bearer("not-a-real-token")
    assert (
        await client.post("/api/chat", json={"message": "hi"}, headers=forged)
    ).status_code == 401
    login = (await sign_in(client)).json()["access_token"]
    as_session = await client.post("/api/chat", json={"message": "hi"}, headers=bearer(login))
    assert as_session.status_code == 401


async def test_chat_uses_the_scope_from_the_token(client, services):
    token = await start_recipient_chat(client)
    response = await client.post(
        "/api/chat", json={"message": "Give updates", "hidden": True}, headers=bearer(token)
    )
    assert response.json() == {"reply": "It is in transit to Lyon."}
    session, text, hidden = services.assistant.calls[0]
    assert session.context.tracking_number == TRACKED and text == "Give updates" and hidden


@pytest.mark.parametrize("message", ["", "   ", "x" * 1001])
async def test_chat_validates_the_message(client, message):
    token = await start_recipient_chat(client)
    response = await client.post("/api/chat", json={"message": message}, headers=bearer(token))
    assert response.status_code == 422


async def test_assistant_outage_is_a_503_with_a_readable_message(client, services):
    services.assistant.error = AssistantUnavailable()
    token = await start_recipient_chat(client)
    response = await client.post("/api/chat", json={"message": "hi"}, headers=bearer(token))
    assert response.status_code == 503
    assert "try again" in response.json()["detail"]


def parse_sse(body: str) -> list[tuple[str, dict]]:
    events = []
    for block in body.strip().split("\n\n"):
        lines = dict(line.split(": ", 1) for line in block.splitlines())
        events.append((lines["event"], json.loads(lines["data"])))
    return events


async def test_streaming_reply(client):
    token = await start_recipient_chat(client)
    response = await client.post(
        "/api/chat/stream", json={"message": "Where is it?"}, headers=bearer(token)
    )
    assert response.headers["content-type"].startswith("text/event-stream")
    assert parse_sse(response.text) == [
        ("status", {"text": "Checking the shipment records…"}),
        ("token", {"text": "It is "}),
        ("token", {"text": "in transit."}),
        ("done", {"reply": "It is in transit."}),
    ]


async def test_streaming_outage_ends_with_an_error_event(client, services):
    services.assistant.error = AssistantUnavailable()
    token = await start_recipient_chat(client)
    response = await client.post("/api/chat/stream", json={"message": "hi"}, headers=bearer(token))
    events = parse_sse(response.text)
    assert events[-1][0] == "error" and "try again" in events[-1][1]["message"]


async def test_history(client, services):
    assert (await client.get("/api/chat/history")).status_code == 401
    token = await start_recipient_chat(client)
    response = await client.get("/api/chat/history", headers=bearer(token))
    assert response.json() == {
        "messages": [{"role": "assistant", "content": "It is in transit to Lyon."}],
        "summarized": True,
    }


async def test_cors_allows_the_frontend_origin_only(client):
    def preflight(origin):
        return client.options(
            "/api/chat",
            headers={"Origin": origin, "Access-Control-Request-Method": "POST"},
        )

    allowed = await preflight("http://localhost:5173")
    assert allowed.headers["access-control-allow-origin"] == "http://localhost:5173"
    blocked = await preflight("https://evil.example")
    assert "access-control-allow-origin" not in blocked.headers

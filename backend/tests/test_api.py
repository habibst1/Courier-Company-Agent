"""HTTP behaviour with the database and the assistant replaced by fakes."""

import pytest
from helpers import offline_settings
from httpx import ASGITransport, AsyncClient

from app.agent.assistant import AssistantUnavailable
from app.main import create_app
from app.security import SessionTokens
from app.services import Services

TRACKED = "TN4255-8215-9617"
PROFILE = {
    "username": "habib_bencheikhali",
    "full_name": "Habib BEN CHEIKH ALI",
    "email": "habib.bencheikh@email.com",
    "phone": "+21624123456",
}


class FakeDB:
    async def ping(self):
        return True

    async def tracking_number_exists(self, tracking_number):
        return tracking_number == TRACKED

    async def customer_profile(self, user_id):
        return PROFILE if user_id == 1 else None


class FakeAssistant:
    def __init__(self):
        self.calls = []
        self.error = None

    async def reply(self, session, text, *, hidden=False):
        self.calls.append((session, text, hidden))
        if self.error:
            raise self.error
        return "It is in transit to Lyon."


@pytest.fixture
def services():
    settings = offline_settings()
    return Services(
        settings=settings,
        db=FakeDB(),
        tokens=SessionTokens(settings.session_secret.get_secret_value(), 1),
        assistant=FakeAssistant(),
    )


@pytest.fixture
async def client(services):
    app = create_app(services=services)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
        yield http


async def start_recipient_chat(client):
    response = await client.post(
        "/api/sessions", json={"mode": "recipient", "tracking_number": TRACKED}
    )
    return response.json()["session_token"]


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


async def test_customer_session_uses_the_server_side_customer(client, services):
    response = await client.post("/api/sessions", json={"mode": "customer", "user_id": 2})
    body = response.json()
    assert body["customer"]["username"] == "habib_bencheikhali"
    assert services.tokens.read(body["session_token"]).context.user_id == 1  # user_id ignored


async def test_chat_requires_a_valid_session(client):
    assert (await client.post("/api/chat", json={"message": "hi"})).status_code == 401
    forged = {"Authorization": "Bearer not-a-real-token"}
    assert (
        await client.post("/api/chat", json={"message": "hi"}, headers=forged)
    ).status_code == 401


async def test_chat_uses_the_scope_from_the_token(client, services):
    token = await start_recipient_chat(client)
    response = await client.post(
        "/api/chat",
        json={"message": "Give updates", "hidden": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.json() == {"reply": "It is in transit to Lyon."}
    session, text, hidden = services.assistant.calls[0]
    assert session.context.tracking_number == TRACKED and text == "Give updates" and hidden


@pytest.mark.parametrize("message", ["", "   ", "x" * 1001])
async def test_chat_validates_the_message(client, message):
    token = await start_recipient_chat(client)
    response = await client.post(
        "/api/chat", json={"message": message}, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422


async def test_assistant_outage_is_a_503_with_a_readable_message(client, services):
    services.assistant.error = AssistantUnavailable()
    token = await start_recipient_chat(client)
    response = await client.post(
        "/api/chat", json={"message": "hi"}, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 503
    assert "try again" in response.json()["detail"]


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

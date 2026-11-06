import pytest

from app.agent.context import CourierContext
from app.security import ChatSession, InvalidToken, SessionTokens

TOKENS = SessionTokens("x" * 40, max_age_hours=1)
RECIPIENT = ChatSession(
    "thread-1", CourierContext(mode="recipient", tracking_number="TN4255-8215-9617")
)


def test_round_trip_keeps_the_scope():
    assert TOKENS.read(TOKENS.issue(RECIPIENT)) == RECIPIENT


def test_tampered_token_is_rejected():
    token = TOKENS.issue(RECIPIENT)
    payload, _, signature = token.rpartition(".")
    forged = payload[:-2] + ("AA" if payload[-2:] != "AA" else "BB") + "." + signature
    with pytest.raises(InvalidToken):
        TOKENS.read(forged)


def test_token_from_another_secret_is_rejected():
    other = SessionTokens("y" * 40, max_age_hours=1)
    with pytest.raises(InvalidToken):
        TOKENS.read(other.issue(RECIPIENT))


def test_expired_token_is_rejected():
    expired = SessionTokens("x" * 40, max_age_hours=1)
    expired._max_age = -1
    with pytest.raises(InvalidToken):
        expired.read(TOKENS.issue(RECIPIENT))


def test_garbage_is_rejected():
    with pytest.raises(InvalidToken):
        TOKENS.read("not-a-token")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"mode": "customer"},
        {"mode": "customer", "user_id": 1, "tracking_number": "TN1"},
        {"mode": "recipient"},
        {"mode": "recipient", "tracking_number": "TN1", "user_id": 1},
        {"mode": "admin", "user_id": 1},
    ],
)
def test_context_rejects_mixed_or_missing_scopes(kwargs):
    with pytest.raises(ValueError):
        CourierContext(**kwargs)

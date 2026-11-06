"""Signed, expiring chat-session tokens. The browser holds them; only the server can create or
read them, so a client cannot pick whose data a chat reaches."""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from itsdangerous import BadSignature, URLSafeTimedSerializer

from .agent.context import CourierContext


class InvalidToken(Exception):
    """The token is missing, was tampered with, or has expired."""


@dataclass(frozen=True)
class ChatSession:
    thread_id: str
    context: CourierContext


def new_thread_id() -> str:
    return str(uuid.uuid4())


class SessionTokens:
    def __init__(self, secret: str, max_age_hours: int) -> None:
        self._serializer = URLSafeTimedSerializer(secret, salt="courier.chat-session.v1")
        self._max_age = max_age_hours * 3600

    def issue(self, session: ChatSession) -> str:
        ctx = session.context
        return self._serializer.dumps(
            {
                "thread": session.thread_id,
                "mode": ctx.mode,
                "user": ctx.user_id,
                "tracking": ctx.tracking_number,
                "name": ctx.display_name,
            }
        )

    def read(self, token: str) -> ChatSession:
        try:
            data = self._serializer.loads(token, max_age=self._max_age)
            context = CourierContext(
                mode=data["mode"],
                user_id=data["user"],
                tracking_number=data["tracking"],
                display_name=data["name"],
            )
            return ChatSession(thread_id=data["thread"], context=context)
        except (BadSignature, KeyError, TypeError, ValueError) as exc:
            raise InvalidToken from exc

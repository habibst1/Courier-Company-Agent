"""Signed, expiring tokens and password hashing.

The browser holds two kinds of token, each signed with its own salt so one can't stand in for
the other:
  login tokens    prove a customer signed in (who they are);
  session tokens  carry one chat's scope and thread (what that chat may see).
Only the server can create or read either, so a client can't pick whose data a chat reaches.
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from itsdangerous import BadSignature, URLSafeTimedSerializer

from .agent.context import CourierContext


class InvalidToken(Exception):
    """The token is missing, was tampered with, or has expired."""


@dataclass(frozen=True)
class ChatSession:
    thread_id: str
    context: CourierContext


@dataclass(frozen=True)
class Customer:
    user_id: int
    username: str
    full_name: str | None


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


class LoginTokens:
    def __init__(self, secret: str, max_age_hours: int) -> None:
        self._serializer = URLSafeTimedSerializer(secret, salt="courier.customer-login.v1")
        self._max_age = max_age_hours * 3600

    def issue(self, customer: Customer) -> str:
        return self._serializer.dumps(
            {"user": customer.user_id, "username": customer.username, "name": customer.full_name}
        )

    def read(self, token: str) -> Customer:
        try:
            data = self._serializer.loads(token, max_age=self._max_age)
            return Customer(
                user_id=int(data["user"]), username=data["username"], full_name=data["name"]
            )
        except (BadSignature, KeyError, TypeError, ValueError) as exc:
            raise InvalidToken from exc


_hasher = PasswordHasher()
# Checked when the user name doesn't exist, so a wrong name takes as long as a wrong password.
_DUMMY_HASH = _hasher.hash("unused-password-for-timing")


def hash_password(password: str) -> str:
    return _hasher.hash(password)


async def verify_password(password_hash: str | None, password: str) -> bool:
    """Argon2 is deliberately slow, so it runs off the event loop."""

    def check() -> bool:
        try:
            return _hasher.verify(password_hash or _DUMMY_HASH, password) and bool(password_hash)
        except (VerificationError, InvalidHashError):
            return False

    return await asyncio.to_thread(check)

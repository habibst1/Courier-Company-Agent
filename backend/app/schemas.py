"""Request and response bodies of the HTTP API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class _Body(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class LoginRequest(_Body):
    username: str = Field(min_length=1, max_length=120, description="User name or e-mail")
    password: str = Field(min_length=1, max_length=200)


class UserOut(BaseModel):
    username: str
    full_name: str | None = None


class LoginResponse(BaseModel):
    access_token: str
    user: UserOut


class SessionRequest(_Body):
    mode: Literal["customer", "recipient"]
    tracking_number: str | None = Field(default=None, pattern=r"^[A-Za-z0-9-]{4,50}$")

    @model_validator(mode="after")
    def _recipient_needs_tracking_number(self) -> SessionRequest:
        if self.mode == "recipient" and not self.tracking_number:
            raise ValueError("tracking_number is required to track a shipment")
        return self


class CustomerProfile(BaseModel):
    username: str
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None


class SessionResponse(BaseModel):
    session_token: str
    mode: Literal["customer", "recipient"]
    tracking_number: str | None = None
    customer: CustomerProfile | None = None


class ChatRequest(_Body):
    message: str = Field(min_length=1, max_length=1000)
    # Automatic turns the UI doesn't display, such as the first question after tracking.
    hidden: bool = False


class ChatResponse(BaseModel):
    reply: str


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class HistoryResponse(BaseModel):
    messages: list[HistoryMessage]
    # True when older turns were folded into a summary and are no longer shown.
    summarized: bool = False

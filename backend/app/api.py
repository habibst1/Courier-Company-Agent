"""HTTP routes. Every chat call carries a signed session token; the server, never the client,
decides whose data that chat can reach."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .agent.assistant import UNAVAILABLE_MESSAGE, AssistantUnavailable
from .agent.context import CourierContext
from .schemas import (
    ChatRequest,
    ChatResponse,
    CustomerProfile,
    HistoryMessage,
    HistoryResponse,
    LoginRequest,
    LoginResponse,
    SessionRequest,
    SessionResponse,
    UserOut,
)
from .security import ChatSession, Customer, InvalidToken, new_thread_id, verify_password
from .services import Services

router = APIRouter(prefix="/api")
_bearer = HTTPBearer(auto_error=False)


def get_services(request: Request) -> Services:
    return request.app.state.services


ServicesDep = Annotated[Services, Depends(get_services)]
Credentials = Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)]


def current_session(credentials: Credentials, services: ServicesDep) -> ChatSession:
    if credentials is None:
        raise HTTPException(401, "Start a chat session first.")
    try:
        return services.tokens.read(credentials.credentials)
    except InvalidToken:
        raise HTTPException(401, "This chat session has expired. Please start a new one.") from None


SessionDep = Annotated[ChatSession, Depends(current_session)]


@router.get("/health")
async def health(services: ServicesDep) -> dict:
    database = await services.db.ping()
    return {"status": "ok" if database else "degraded", "database": database}


@router.post("/auth/login", response_model=LoginResponse)
async def login(body: LoginRequest, services: ServicesDep) -> LoginResponse:
    row = await services.db.find_login(body.username)
    if not await verify_password(row["password_hash"] if row else None, body.password):
        raise HTTPException(401, "Wrong user name or password.")
    customer = Customer(
        user_id=row["user_id"], username=row["username"], full_name=row["full_name"]
    )
    return LoginResponse(
        access_token=services.logins.issue(customer),
        user=UserOut(username=customer.username, full_name=customer.full_name),
    )


@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    body: SessionRequest, credentials: Credentials, services: ServicesDep
) -> SessionResponse:
    if body.mode == "recipient":
        tracking_number = body.tracking_number.upper()
        if not await services.db.tracking_number_exists(tracking_number):
            raise HTTPException(404, "We couldn't find a shipment with that tracking number.")
        context = CourierContext(mode="recipient", tracking_number=tracking_number)
        token = services.tokens.issue(ChatSession(new_thread_id(), context))
        return SessionResponse(
            session_token=token, mode="recipient", tracking_number=tracking_number
        )

    if credentials is None:
        raise HTTPException(401, "Sign in to chat about your shipments.")
    try:
        customer = services.logins.read(credentials.credentials)
    except InvalidToken:
        raise HTTPException(401, "Your sign-in has expired. Please sign in again.") from None
    profile = await services.db.customer_profile(customer.user_id)
    if profile is None:
        raise HTTPException(401, "This account no longer exists.")
    context = CourierContext(
        mode="customer", user_id=customer.user_id, display_name=profile["full_name"]
    )
    token = services.tokens.issue(ChatSession(new_thread_id(), context))
    return SessionResponse(
        session_token=token, mode="customer", customer=CustomerProfile(**profile)
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, session: SessionDep, services: ServicesDep) -> ChatResponse:
    reply = await services.assistant.reply(session, body.message, hidden=body.hidden)
    return ChatResponse(reply=reply)


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/chat/stream")
async def chat_stream(
    body: ChatRequest, session: SessionDep, services: ServicesDep
) -> StreamingResponse:
    """Server-sent events: status (a lookup is running), token (reply text as it's written),
    done (the complete reply), or error."""

    async def events() -> AsyncIterator[str]:
        try:
            async for kind, text in services.assistant.stream(
                session, body.message, hidden=body.hidden
            ):
                yield _sse(kind, {"reply" if kind == "done" else "text": text})
        except AssistantUnavailable:
            yield _sse("error", {"message": UNAVAILABLE_MESSAGE})

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/chat/history", response_model=HistoryResponse)
async def chat_history(session: SessionDep, services: ServicesDep) -> HistoryResponse:
    messages, summarized = await services.assistant.history(session)
    return HistoryResponse(
        messages=[HistoryMessage(**message) for message in messages], summarized=summarized
    )

"""HTTP routes. Every chat call carries a signed session token; the server, never the client,
decides whose data that chat can reach."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .agent.context import CourierContext
from .schemas import (
    ChatRequest,
    ChatResponse,
    CustomerProfile,
    SessionRequest,
    SessionResponse,
)
from .security import ChatSession, InvalidToken, new_thread_id
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


@router.post("/sessions", response_model=SessionResponse)
async def create_session(body: SessionRequest, services: ServicesDep) -> SessionResponse:
    if body.mode == "recipient":
        tracking_number = body.tracking_number.upper()
        if not await services.db.tracking_number_exists(tracking_number):
            raise HTTPException(404, "We couldn't find a shipment with that tracking number.")
        context = CourierContext(mode="recipient", tracking_number=tracking_number)
        token = services.tokens.issue(ChatSession(new_thread_id(), context))
        return SessionResponse(
            session_token=token, mode="recipient", tracking_number=tracking_number
        )

    user_id = services.settings.demo_customer_id
    profile = await services.db.customer_profile(user_id)
    if profile is None:
        raise HTTPException(503, "The demo customer is missing from the database.")
    context = CourierContext(mode="customer", user_id=user_id, display_name=profile["full_name"])
    token = services.tokens.issue(ChatSession(new_thread_id(), context))
    return SessionResponse(
        session_token=token, mode="customer", customer=CustomerProfile(**profile)
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, session: SessionDep, services: ServicesDep) -> ChatResponse:
    reply = await services.assistant.reply(session, body.message, hidden=body.hidden)
    return ChatResponse(reply=reply)

"""FastAPI application factory. Run it with `python -m app` (see __main__.py)."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .agent.assistant import AssistantUnavailable
from .api import router
from .config import Settings, get_settings
from .services import Services, build_services


def configure_logging(level: str) -> None:
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")
    for noisy in ("httpx", "httpcore", "groq"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def create_app(settings: Settings | None = None, services: Services | None = None) -> FastAPI:
    """Build the app. Tests pass ready-made `services`; otherwise startup builds them."""
    settings = settings or (services.settings if services else get_settings())
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if services is not None:
            yield
            return
        async with build_services(settings) as built:
            app.state.services = built
            yield

    app = FastAPI(title="CourierTrack API", version="2.0.0", lifespan=lifespan)
    if services is not None:
        app.state.services = services
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.include_router(router)

    @app.exception_handler(AssistantUnavailable)
    async def assistant_unavailable(_: Request, __: AssistantUnavailable) -> JSONResponse:
        return JSONResponse(
            {"detail": "The assistant is unavailable right now. Please try again in a moment."},
            status_code=503,
        )

    return app

"""Who a chat is for. The server sets this from a signed session token; tools read it through
ToolRuntime, so the model never sees it and cannot change it."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Mode = Literal["customer", "recipient"]


@dataclass(frozen=True)
class CourierContext:
    mode: Mode
    user_id: int | None = None
    tracking_number: str | None = None
    display_name: str | None = None

    def __post_init__(self) -> None:
        if self.mode == "customer":
            if self.user_id is None or self.tracking_number is not None:
                raise ValueError("a customer context needs a user_id and no tracking_number")
        elif self.mode == "recipient":
            if not self.tracking_number or self.user_id is not None:
                raise ValueError("a recipient context needs a tracking_number and no user_id")
        else:
            raise ValueError(f"unknown mode {self.mode!r}")

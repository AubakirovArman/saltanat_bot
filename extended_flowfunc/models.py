from __future__ import annotations
from typing import Any
from pydantic import Field
import flowfunc.models as fm

class Node(fm.Node):
    """Extended Node model supporting additional customization options."""

    icon: str | None = None
    style: dict[str, Any] | None = None
    extra: dict[str, Any] | None = Field(default=None, description="Arbitrary node settings")

class Port(fm.Port):
    """Extended Port model with optional styling."""

    style: dict[str, Any] | None = None

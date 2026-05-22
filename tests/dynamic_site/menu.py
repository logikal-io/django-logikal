from dataclasses import dataclass, field
from typing import Any


@dataclass
class MenuItem:
    title: str
    view_name: str = None
    view_kwargs: dict[str, Any] = None
    submenu: list['MenuItem'] = None

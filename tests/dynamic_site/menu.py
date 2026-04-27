from dataclasses import dataclass, field
from typing import Any


@dataclass
class MenuItem:
    title: str
    view_name: str = field(default_factory=str)
    view_kwargs: dict[str, Any] = field(default_factory=dict)
    submenu: list['MenuItem'] = field(default_factory=list)

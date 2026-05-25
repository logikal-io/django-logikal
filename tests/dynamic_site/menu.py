from dataclasses import dataclass
from typing import Any


@dataclass
class MenuItem:
    title: str
    view_name: str = None
    view_kwargs: dict[str, Any] = None
    submenu: list['MenuItem'] = None
    id: str = None

    def __post_init__(self):
        if self.id is None:
            self.id = self.title.lower().replace(' ', '_')

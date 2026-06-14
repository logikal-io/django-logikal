from dataclasses import dataclass
from typing import Any


@dataclass
class MenuItem:
    title: str
    view_name: str = None
    view_kwargs: dict[str, Any] = None
    submenu: list['MenuItem'] = None
    id: str = None
    id_prefix: str = 'id_menu'

    def __post_init__(self):
        if self.view_kwargs is None:
            self.view_kwargs = {}

        if self.id is None:
            self.id = self.id_prefix + '_' + self.title.lower().replace(' ', '_')

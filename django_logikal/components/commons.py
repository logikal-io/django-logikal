from dataclasses import dataclass, field
from typing import Any


@dataclass
class MenuItem:
    """
    An item in a menu bar.
    """
    title: str
    view_name: str | None = None
    view_kwargs: dict[str, Any] = field(default_factory=dict)
    submenu: list['MenuItem'] = field(default_factory=list)
    id: str | None = None
    id_prefix: str = 'id_menu'

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = self.id_prefix + '_' + self.title.lower().replace(' ', '_')

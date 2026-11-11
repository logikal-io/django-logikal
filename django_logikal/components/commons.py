from dataclasses import dataclass, field
from typing import Any


@dataclass
class MenuItem:
    """
    An item in a menu rendered as a menu button.
    """
    title: str
    view_name: str | None = None
    view_kwargs: dict[str, Any] = field(default_factory=dict)
    submenu: list['MenuItem | MenuCustomItem'] = field(default_factory=list)
    id: str | None = None
    classes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = self.title.lower().replace(' ', '-').replace('_', '-')


@dataclass
class MenuCustomItem:
    """
    An item in a menu rendered as custom content.
    """
    content: str

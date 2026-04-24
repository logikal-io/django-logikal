from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class MenuItem:
    title: str
    view_name: str
    kwargs: Dict[str, Any] = field(default_factory=dict)
    sublinks: list[Any] = field(default_factory=list)


menu_items = [
    MenuItem(title="Home", view_name="dynamic_site:home"),
    MenuItem(title="Errors", view_name="error:404",
             sublinks=[
                 MenuItem(title="400", view_name="error:400"),
                 MenuItem(title="403", view_name="error:403"),
                 MenuItem(title="404", view_name="error:404"),
                 MenuItem(title="500", view_name="error:500"),
             ]
             ),
    MenuItem(title="Templates", view_name="dynamic_site:templates",
             kwargs={'arg': 'extensions'}),
    MenuItem(title="API", view_name="api-root"),
]

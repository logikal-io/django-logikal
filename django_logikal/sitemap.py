from typing import Mapping, Sequence

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap[str]):
    i18n = True
    alternates = True
    x_default = True

    def __init__(self, path_priority: Mapping[str, str]):
        self.path_priority = path_priority

    def items(self) -> Sequence[str]:
        return list(self.path_priority.keys())

    def priority(self, item: str) -> Sequence[str]:
        return self.path_priority[item]

    @staticmethod
    def location(item: str) -> str:
        return reverse(item)

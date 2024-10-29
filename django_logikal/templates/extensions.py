import zoneinfo

from django.utils import timezone, translation
from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.parser import Parser
from jinja2.runtime import Macro


class LanguageExtension(Extension):
    tags = {'language'}

    def parse(self, parser: Parser) -> nodes.Node:
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(tuple(['name:endlanguage']), drop_needle=True)
        block = nodes.CallBlock(self.call_method('_override_language', args), [], [], body)
        return block.set_lineno(lineno)

    @staticmethod
    def _override_language(language_code: str, caller: Macro) -> str:
        with translation.override(language_code):
            return caller()


class TimeZoneExtension(Extension):
    tags = {'timezone'}

    def parse(self, parser: Parser) -> nodes.Node:
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(tuple(['name:endtimezone']), drop_needle=True)
        block = nodes.CallBlock(self.call_method('_override_timezone', args), [], [], body)
        return block.set_lineno(lineno)

    @staticmethod
    def _override_timezone(zone_id: str, caller: Macro) -> str:
        current_timezone = timezone.get_current_timezone()
        try:
            timezone.activate(zoneinfo.ZoneInfo(zone_id))
            return caller()
        finally:
            timezone.activate(current_timezone)

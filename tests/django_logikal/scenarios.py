from dataclasses import replace

from pytest_logikal import scenarios

desktop = replace(scenarios.desktop, languages=['en-us'])
desktop_all_languages = replace(scenarios.desktop, languages=None)

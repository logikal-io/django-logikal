from dataclasses import replace

from pytest_logikal import scenarios

desktop = replace(scenarios.desktop, languages=['en-us'])
mobile_l = replace(scenarios.mobile_l, languages=['en-us'])
desktop_all_languages = replace(scenarios.desktop, languages=None)

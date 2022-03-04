from typing import Set, Dict

from libssettings.utils import is_integer
from libssettings.exceptions import SSettingsError

class InvalidSettingValueError(SSettingsError):
    pass

class Rule:
    def validate(self, value: str) -> None:
        raise NotImplementedError

class OptionsRule(Rule):
    def __init__(self, options: Set[str]) -> None:
        self._options = options
    
    def validate(self, value: str) -> None:
        if value not in self._options:
            raise InvalidSettingValueError(f'Invalid value {repr(value)}, must be one of: {repr(self._options)}')

class IntegerRule(Rule):
    def validate(self, value: str) -> None:
        if not is_integer(value):
            raise InvalidSettingValueError(f'Invalid value {repr(value)}, must be an integer')

class PositiveIntegerRule(Rule):
    def validate(self, value: str) -> None:
        if not (is_integer(value) and int(value) >= 0):
            raise InvalidSettingValueError(f'Invalid value {repr(value)}, must be a positive integer')

class NegativeIntegerRule(Rule):
    def validate(self, value: str) -> None:
        if not (is_integer(value) and int(value) <= 0):
            raise InvalidSettingValueError(f'Invalid value {repr(value)}, must be a negative integer')

class Rules:
    _rules: Dict[str, Rule]

    def __init__(self) -> None:
        self._rules = dict()
    
    def set(self, key: str, rule: Rule) -> None:
        self._rules[key] = rule

    def reset(self, key: str) -> None:
        self._rules.pop(key, None)

    def validate(self, key: str, value: str) -> None:
        rule = self._rules.get(key)
        if rule is not None:
            rule.validate(value)

import pprint
from typing import Dict, List

from libssettings.exceptions import SSettingsError

class Settings:
    _values: Dict[str, str]

    def __init__(self) -> None:
        self._values = dict()

    def get(self, key: str) -> str:
        value = self._values.get(key)
        if value is None:
            raise SSettingsError(f'No value found for key "{key}"')
        return value

    def set(self, key: str, value: str) -> None:
        self._values[key] = value

    def dump(self) -> str:
        return pprint.pformat(self._values)

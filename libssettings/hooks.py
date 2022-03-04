import pprint
from typing import Dict, List

from libssettings.exceptions import SSettingsError

class Hooks:
    _hooks: Dict[str, List[str]]

    def __init__(self) -> None:
        self._hooks = dict()

    def get(self, key: str) -> List[str]:
        return self._hooks.get(key) or []

    def new(self, key: str, exec_string: str) -> None:
        self._hooks[key] = self.get(key) + [exec_string]
    
    def reset(self, key: str) -> None:
        self._hooks.pop(key, None)

    def dump(self) -> str:
        return pprint.pformat(self._hooks)

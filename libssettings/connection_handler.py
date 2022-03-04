import os
import subprocess
from typing import List, Callable

from libssettings.hooks import Hooks
from libssettings.logger import Logger
from libssettings.settings import Settings
from libssettings.connection import Connection
from libssettings.exceptions import SSettingsError, QuitException

class ConnectionHandler:
    def handle_connection(self, connection: Connection) -> None:
        raise NotImplementedError

HELP_MESSAGE = """\
usage: ssettings COMMAND

Controls the settings daemon by communicating with it through a socket.

general commands:
    get KEY       - Get the settings value for KEY.
    set KEY VALUE - Set the settings value for KEY to VALUE.
    dump          - Dump all current settings.
    help          - Show this help message and exit.
    quit          - Ask ssettingsd to suicide.

hook commands:
    hook new KEY EXEC - Create a new hook (EXEC) for KEY.
    hook reset KEY    - Remove all hook for KEY.
    hook get KEY      - Show all hooks for KEY.
    hook dump         - Show all current existing hooks
"""

class SSettingsConnectionHandler(ConnectionHandler):
    _settings: Settings
    _hooks: Hooks
    _logger: Logger
    _socket_path: str

    def __init__(self, logger: Logger, settings: Settings, hooks: Hooks, socket_path: str) -> None:
        self._settings = settings
        self._logger = logger
        self._hooks = hooks
        self._socket_path = socket_path
    
    def _handle_no_arguments(self, args: List[str], connection: Connection) -> None:
        raise SSettingsError('No arguments given')
    
    def _handle_unknown_command(self, args: List[str], connection: Connection) -> None:
        raise SSettingsError(f'Unknown command {repr(args[0])}')
    
    def _handle_get(self, args: List[str], connection: Connection) -> None:
        if len(args) != 2:
            raise SSettingsError('Invalid arguments (expected 1)')
        connection.send(self._settings.get(args[1]))

    def _execute_hooks(self, key: str, value: str) -> None:
        for hook in self._hooks.get(key):
            env_copy = os.environ.copy()
            env_copy['SSETTINGS_SOCKET'] = self._socket_path
            env_copy['SSETTINGS_KEY'] = key
            env_copy['SSETTINGS_VALUE'] = value
            subprocess.Popen(['sh', '-c', hook], env=env_copy)

    def _handle_set(self, args: List[str], connection: Connection) -> None:
        if len(args) != 3:
            raise SSettingsError('Invalid arguments (expected 2)')
        key, value = args[1], args[2]
        self._settings.set(key, value)
        self._execute_hooks(key, value)

    def _handle_dump(self, args: List[str], connection: Connection) -> None:
        if len(args) != 1:
            raise SSettingsError('Invalid arguments (expected 0)')
        connection.send(self._settings.dump())
        
    def _handle_help(self, args: List[str], connection: Connection) -> None:
        if len(args) != 1:
            raise SSettingsError('Invalid arguments (expected 0)')
        connection.send(HELP_MESSAGE)
    
    def _handle_quit(self, args: List[str], connection: Connection) -> None:
        raise QuitException

    def _handle_hook_no_arguments(self, args: List[str], connection: Connection) -> None:
        raise SSettingsError('No arguments given to "hook" subcommand')

    def _handle_hook_unknown_subcommand(self, args: List[str], connection: Connection) -> None:
        raise SSettingsError(f'Unknown hook subcommand {repr(args[1])}')

    def _handle_hook_new(self, args: List[str], connection: Connection) -> None:
        if len(args) != 4:
            raise SSettingsError('Invalid arguments (expected 2)')
        self._hooks.new(args[2], args[3])

    def _handle_hook_reset(self, args: List[str], connection: Connection) -> None:
        if len(args) != 3:
            raise SSettingsError('Invalid arguments (expected 1)')
        self._hooks.reset(args[2])

    def _handle_hook_get(self, args: List[str], connection: Connection) -> None:
        if len(args) != 3:
            raise SSettingsError('Invalid arguments (expected 1)')
        hook = self._hooks.get(args[2])
        if len(hook) > 0:
            connection.send('\n'.join(hook))

    def _handle_hook_dump(self, args: List[str], connection: Connection) -> None:
        if len(args) != 2:
            raise SSettingsError('Invalid arguments (expected 0)')
        connection.send(self._hooks.dump())

    def _get_hook_handler(self, args: List[str]) -> Callable[[List[str], Connection], None]:
        return self._handle_hook_no_arguments if len(args) == 1 else {
            'new': self._handle_hook_new,
            'reset': self._handle_hook_reset,
            'get': self._handle_hook_get,
            'dump': self._handle_hook_dump,
        }.get(args[1]) or self._handle_hook_unknown_subcommand

    def _handle_hook(self, args: List[str], connection: Connection) -> None:
        self._get_hook_handler(args)(args, connection)

    def _get_handler(self, args: List[str]) -> Callable[[List[str], Connection], None]:
        return self._handle_no_arguments if len(args) == 0 else {
            'get': self._handle_get,
            'set': self._handle_set,
            'dump': self._handle_dump,
            'help': self._handle_help,
            'quit': self._handle_quit,
            'hook': self._handle_hook,
        }.get(args[0]) or self._handle_unknown_command
    
    def handle_connection(self, connection: Connection) -> None:
        args = connection.recv_args()
        self._logger.log('Args:', args)
        try:
            self._get_handler(args)(args, connection)
        except SSettingsError as e:
            connection.send_error(str(e))

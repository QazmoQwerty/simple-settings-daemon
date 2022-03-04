from typing import List, Callable

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

commands:
    get    - Get a settings value.
    set    - Set a settings value.
    dump   - Dump all current settings.
    help   - Show this help message and exit.
    quit   - Ask ssettingsd to suicide.
"""

class SSettingsConnectionHandler(ConnectionHandler):
    _settings: Settings
    _logger: Logger

    def __init__(self, logger: Logger, settings: Settings) -> None:
        self._settings = settings
        self._logger = logger
    
    def _handle_no_arguments(self, args: List[str], connection: Connection) -> None:
        raise SSettingsError('No arguments given')
    
    def _handle_unknown_command(self, args: List[str], connection: Connection) -> None:
        raise SSettingsError(f'Unknown command {repr(args[0])}')
    
    def _handle_get(self, args: List[str], connection: Connection) -> None:
        if len(args) != 2:
            raise SSettingsError('Invalid arguments (expected 1)')
        connection.send(self._settings.get(args[1]))

    def _handle_set(self, args: List[str], connection: Connection) -> None:
        if len(args) != 3:
            raise SSettingsError('Invalid arguments (expected 2)')
        self._settings.set(args[1], args[2])

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

    def _get_handler(self, args: List[str]) -> Callable[[List[str], Connection], None]:
        return self._handle_no_arguments if len(args) == 0 else {
            'get': self._handle_get,
            'set': self._handle_set,
            'dump': self._handle_dump,
            'help': self._handle_help,
            'quit': self._handle_quit,
        }.get(args[0]) or self._handle_unknown_command
    
    def handle_connection(self, connection: Connection) -> None:
        args = connection.recv_args()
        self._logger.log('Args:', args)
        try:
            self._get_handler(args)(args, connection)
        except SSettingsError as e:
            connection.send_error(str(e))

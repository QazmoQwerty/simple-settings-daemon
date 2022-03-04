from typing import NamedTuple
from argparse import ArgumentParser

from libssettings.hooks import Hooks
from libssettings.logger import Logger
from libssettings.settings import Settings
from libssettings.version import VERSION
from libssettings.server import UnixSocketServer
from libssettings.exceptions import QuitException
from libssettings.connection_handler import SSettingsConnectionHandler

class CmdArguments(NamedTuple):
    socket_path: str
    verbose: bool

def parse_arguments() -> CmdArguments:
    parser = ArgumentParser(description='Daemon process for ssettings')
    parser.add_argument(
        '-v', '--version',
        action = 'version',
        version = VERSION,
        help = 'Show version number and exit'
    )
    parser.add_argument(
        '-V', '--verbose',
        action = 'store_true',
        help = 'Enable verbose output'
    )
    parser.add_argument(
        '-s', '--socket',
        type = str,
        default = '/tmp/ssettings_socket',
        help = f'Socket to listen for incoming connections'
    )
    args = parser.parse_args()
    return CmdArguments(
        socket_path = args.socket,
        verbose = args.verbose
    )

def run():
    cmd_arguments = parse_arguments()
    logger = Logger(cmd_arguments.verbose)
    settings = Settings()
    hooks = Hooks()
    connection_handler = SSettingsConnectionHandler(logger, settings, hooks, cmd_arguments.socket_path)
    with UnixSocketServer(cmd_arguments.socket_path, connection_handler) as server:
        server.run()

def main() -> int:
    try:
        run()
    except QuitException:
        return 0
    return 1

if __name__ == '__main__':
    exit(main())

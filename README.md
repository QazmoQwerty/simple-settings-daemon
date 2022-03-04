# simple-settings-daemon

Simple settings daemon for linux.

## Usage

See [the manpage](docs/manpage.md) for a more detailed explanation.

### ssettingsd

```
usage: ssettingsd [-h] [-v] [-V] [-s SOCKET]

Daemon process for ssettings

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show version number and exit
  -V, --verbose         Enable verbose output
  -s SOCKET, --socket SOCKET
                        Socket to listen for incoming connections
```

### ssettings

```
usage: ssettings COMMAND

Controls the settings daemon by communicating with it through a socket.

general commands:
    get KEY       - Get the settings value for KEY.
    set KEY VALUE - Set the settings value for KEY to VALUE.
    dump          - Dump all current settings.
    help          - Show this help message and exit.
    quit          - Ask ssettingsd to suicide.

rule commands:
    rule KEY int          - Allow only integers for KEY
    rule KEY int-positive - Allow only positive integers for KEY
    rule KEY int-negative - Allow only negative integers for KEY
    rule KEY values VALUE1[,...] - Allow only specific values for KEY (case sensitive!)

hook commands:
    hook new KEY EXEC - Create a new hook (EXEC) for KEY.
    hook reset KEY    - Remove all hook for KEY.
    hook get KEY      - Show all hooks for KEY.
    hook dump         - Show all current existing hooks
```

## Requirements

* bspwm

## Installation

Install from pypi:

```
sudo pip3 install simplesettingsdaemon
```

Build and install from source:

```sh
git clone https://github.com/QazmoQwerty/simple-settings-daemon
cd simple-settings-daemon
sudo pip3 install -r requirements.txt
python3 -m build
sudo python3 -m pip install dist/simplesettingsdaemon*.whl
```
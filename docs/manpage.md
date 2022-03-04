% PALETTE(1) Palette 0.0.2
% Shalev Don Meiri
% March 4, 2022

# NAME

ssettingsd - Simple settings daemon for linux.

# SYNOPSIS

ssettingsd [ -h | -v | -V | -s SOCKET ]

ssettings COMMAND [*OPTIONS*]

# DESCRIPTION

The settings daemon simply holds a mapping of keys to values, which are all strings (both key and value). It starts out empty, and you can add new setting values with `ssettings set KEY VALUE`.

# USAGE

## SSETTINGSD

-h, \--help
:   Show help message and exit.

-v, \--version
:   Show version and exit.

-V, \--verbose
:   Enable verbose output.

-s, \--socket
:   Socket to listen for incoming connections.

## SSETTINGS

Controls the settings daemon by communicating with it through a socket.

get KEY
:   Get the settings value for KEY.

set KEY VALUE
:   Set the settings value for KEY to VALUE.

dump         
:   Dump all current settings.

help         
:   Show this help message and exit.

quit         
:   Ask `ssettingsd` to suicide.

rule KEY int
:   Allow only integers for KEY

rule KEY int-positive
:   Allow only positive integers for KEY

rule KEY int-negative
:   Allow only negative integers for KEY

rule KEY values VALUE1[,...]
:   Allow only specific values for KEY (case sensitive!)

hook new KEY EXEC
:   Create a new hook (EXEC) for KEY.

hook reset KEY   
:   Remove all hook for KEY.

hook get KEY     
:   Show all hooks for KEY.

hook dump        
:   Show all current existing hooks

### Hooking

You can add command strings to run whenever the a certain key `set`. Each key can have multiple hooks. These hooks will be executed with `sh -c`, with the following Enviroment Variables set:

* SSETTINGS_SOCKET - the socket to which `ssettingsd` is listening.

* SSETTINGS_KEY    - the key which was `set`

* SSETTINGS_VALUE  - the value which was `set`

# SEE ALSO

Source code can be found here: 
<https://github.com/QazmoQwerty/simple-settings-daemon>

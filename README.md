# Regioneer

The general purpose of the application is to provide an abstraction of location, based on user defined parameters, that will then invoke actions that modify the system's behavior. This is especially useful in home vs work settings.

## Master Use Case:

User X has 2 monitors at work, but has one monitor at home. Everytime the user goes to work he has to setup his monitors manually the way he likes them.

Solution: Define a profile for 'work' and allow the execution of system modifications to get the desired environment.

# How to determine 'location':

## Requirements:

# GPS
..* % variance <user specified>
# Provider <geoclue 1 / geoclue 2>
..* Need check existence of geo clue
..* Fallback: google location based IP
# Connected Wifi
..* Surrounding Wifi Networks
..* Connected Wifi Network
# Connected eth
..* Device
..* Must have IP
..* Pingable network location <public/private>
..* Public <Default: Google, opt: (user specified) >
..* Private <user specified>

Existence of specific ephemeral object
Pingable public server
Pingable private server
Attached device
Keyboard
Monitors
Mice
Printers
Hard drives
Custom
Must specify specific device ID


What actions are available:

For the initial alpha release, this will just provide an entry for invoking a user specified script.

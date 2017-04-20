# Regioneer

The general purpose of the application is to provide an abstraction of location, based on user defined parameters, that will then invoke actions that modify the system's behavior. This is especially useful in home vs work settings.

NOTE: This is very much in design phase, and more than likely, won't work for you.

## Master Use Case:

User X has 2 monitors at work, but has one monitor at home. Everytime the user goes to work he has to setup his monitors manually the way the user likes them.

Solution: Define a profile for 'work' and allow the execution of system modifications to get the desired environment.

## Development Requirements

This was written for Python 3, and requires NetworkManager to be installed as well as the netifaces and pytest for unittests.

# How Regioneer determines 'location':

## Design Requirements:

Each bullet point is a main source of determining your 'location'. Do notice that GPS is only one aspect, GPS alone is not good enough to determine the master usecase for different work areas within a work or home setting.

* GPS
    * % variance <user specified>
    * Provider <geoclue 1 / geoclue 2>
        * Need to check existence of geo clue
        * Fallback: google location based IP

* Connected Wifi
    * (Required) Device
    * (Required) IP
    * (Required) Connected Wifi Network
    * (Optional) Surrounding Wifi Networks with threshold

* Connected eth
    * (Required) Device
    * (Required) Must have IP
    * (Optional) Pingable network location <public/private>
    * (Optional) Pingable Public <Default: Google, opt: (user specified) >
    * (Optional) Pingable Private <user specified>

* Existence of specific ephemeral object
    * Pingable server (public or private, preferred: private)
    * Attached device
    * Keyboard
    * Monitors
    * Mice
    * Printers
    * Hard drives
    * Custom
        * Must specify specific device ID


# What actions are available:

For the initial alpha release, this will just provide an entry for invoking a user specified script.
""" Constants file for regioneers core module """

###########################
# Constant/Variable names #
###########################

CONFIG  = "config"
LINUX   = "linux"
DARWIN  = "darwin"
WINDOWS = "windows"

###############################
# Configuration File Location #
###############################

LINUX_CONFIG_HOME   = "$HOME/.config/regioneer.json"
DARWIN_CONFIG_HOME  = "$HOME/Library/ApplicationSupport/regioneer.json"
WINDOWS_CONFIG_HOME = "%USERPROFILE%\\regioneer.json"

BASE_CONFIGS = {
    LINUX: {
        CONFIG: LINUX_CONFIG_HOME
    },
    DARWIN: {
        CONFIG: DARWIN_CONFIG_HOME
    },
    WINDOWS: {
        CONFIG: WINDOWS_CONFIG_HOME
    }
}


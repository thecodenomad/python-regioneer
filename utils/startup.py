import json
import os
import sys
from textwrap import indent

from subprocess import check_output
from core.models import load_models_from_configuration
from utils.logger import get_logger
from shutil import copyfile

_log = get_logger()

DEFAULT_LOC = "$HOME/.config/regioneer.json"
REGIONEER_LOC = os.path.dirname(__file__)


def load_configuration_file(loc=DEFAULT_LOC):
    """ Load a given configuration file based on the passed in location """

    if not loc:
        print("'{}' is not supported (yet?)...".format(curr_sys))
        sys.exit(1)

    # Load configuration file if exist
    loc = os.path.expandvars(loc)

    _log.info("Looking for configuration file at: {}".format(loc))

    if os.path.exists(loc):
        with open(loc, 'r') as infile:
            conf = json.load(infile)
            return load_models_from_configuration(conf)

    # Else Create simple configuration file
    else:
        file_loc = "{}/../configs/default.json".format(REGIONEER_LOC)
        _log.info("No config found, copying default {} to {}".format(file_loc, loc))
        copyfile(file_loc, loc)
        return load_configuration_file(loc)


def main():
    # See what type of system this is
    print(os.uname())
    curr_sys = os.uname().sysname.lower()
    curr_sys = curr_sys.lower()
    conf_loc = constants.BASE_CONFIGS.get(curr_sys, None)

    # Fail if we don't find our system
    if not conf_loc:
        _log.error("Couldn't determine the standard conf storage for your system: '{}'".format(curr_sys))
        sys.exit(1)

    conf_loc = conf_loc[constants.CONFIG]

    # Load the configuration
    profiles = load_configuration_file(conf_loc)

    guessed_profiles = []

    # These should be profile objects at this point
    for profile in profiles:
        _log.info("Checking to see if {} is the active profile".format(profile.name))
        if profile.is_active():
            guessed_profiles.append(profile)

    _log.info("Guessed the following active profiles: {}".format([p.name for p in guessed_profiles]))
    for profile in guessed_profiles:
        _log.info("Profile '{}' requires executing: \"{}\":".format(profile.name, profile.executable))

        # Subprocess requires and array
        executable = profile.executable
        opts = executable.split()
        output = check_output(opts).decode('utf-8')
        print("{}".format(indent(output, prefix="  ")))
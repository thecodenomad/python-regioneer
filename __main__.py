#!/usr/bin/python
""" Main module for starting regioneer program """

import json
import os
from pprint import pprint
import sys

from regioneer.core import constants
from regioneer.core.models import load_models_from_configuration

def load_configuration_file(loc):
    """ Load a given configuration file based on the passed in location """

    if not loc:
        print("'{}' is not supported (yet?)...".format(curr_sys))
        sys.exit(1)

    # Load configuration file if exist

    loc = os.path.expandvars(loc)

    print("Looking for configuration file at: {}".format(loc))

    if os.path.exists(loc):
        with open(loc, 'r') as infile:
            print(infile)
            conf = json.load(infile)
            print("Found a config")
            pprint(conf)
            print("Trying to load configuration...")
            return load_models_from_configuration(conf)

    # Else Create simple configuration file
    else:
        # TODO: when a configuration file doesn't already exist copy over the base configuration
        pass

if __name__ == "__main__":

    # See what type of system this is
    print(os.uname())
    curr_sys = os.uname().sysname.lower()
    curr_sys = curr_sys.lower()
    conf_loc = constants.BASE_CONFIGS.get(curr_sys, None)

    # Fail if we don't find our system
    if not conf_loc:
        print("Couldn't determine the standard conf storage for your system: '{}'".format(curr_sys))
        sys.exit(1)

    conf_loc = conf_loc[constants.CONFIG]

    # Load the configuration
    profiles = load_configuration_file(conf_loc)

    guessed_profiles = []

    # These should be profile objects at this point
    for profile in profiles:
        print("Checking to see if {} is the active profile".format(profile.name))
        if profile.is_active():
            guessed_profiles.append(profile)

    print("Guessed the following active profiles: ")
    for profile in guessed_profiles:
        print("{}".format(profile.name()))

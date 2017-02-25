#!/usr/bin/python
""" Main module for starting regioneer program """

import json
import os
from pprint import pprint
import sys

from subprocess import check_output

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
            conf = json.load(infile)
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

    print("Guessed the following active profiles: {}".format([p.name for p in guessed_profiles]))
    for profile in guessed_profiles:
        print("Profile '{}' requires executing: \"{}\"".format(profile.name, profile.executable))

        # Subprocess requires and array
        executable = profile.executable
        opts = executable.split()
        output = check_output(opts).decode('utf-8')
        print("Output from execution: {}".format(output))



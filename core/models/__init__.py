""" Models modules meant to create simple simulated models for location hints """

from regioneer.core.hints import HintFactory, constants


def load_hint(hint):
    """ Loads a hint from a configuration object """


def load_models_from_configuration(conf):
    """ Load a configuration from a parsed JSON config file which should be in dictionary form here
    :param conf: dictionary of regioneer configurations
    :return profiles: Object representation of the location hints specified in the configuration file
    """

    profiles = []

    for name, hints in conf.items():

        # Setup a blank profile
        profile = Profile(name, hints=[])

        for hint in hints:
            location_hint = HintFactory.factory(hint[constants.HINT_TYPE], hint)
            profile.add_hint(location_hint)

        profiles.append(profile)

    return profiles


class Profile(object):
    """ Profile object that stores the configuration settings for a given regioneer profile. """

    def __init__(self, name, hints=None):
        """ Initialize """
        self._name = name
        self._hints = hints or []

    @property
    def name(self):
        """ Return the name of the profile """
        return self._name

    @name.setter
    def name(self, name):
        """ Set a name property for the profile """
        self._name = name

    @property
    def hints(self):
        """ Hints getter """
        return self._hints

    @hints.setter
    def hints(self, hints):
        """ Hints setter """
        self._hints = hints

    def add_hint(self, hint):
        self._hints.append(hint)

    def is_active(self):
        """ Checks to see if this given profile is active. """

        # Go through all the hints and check to see if they are active, if all of them are active then
        # we have an active profile

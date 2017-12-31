""" Models modules meant to create simple simulated models for location hints """

from core.hints import HintFactory, constants

from utils.logger import get_logger
from utils.borg import Borg

import uuid

_log = get_logger()

def load_hint(hint):
    """ Loads a hint from a configuration object """


def load_models_from_configuration(conf):
    """ Load a configuration from a parsed JSON config file which should be in dictionary form here
    :param conf: dictionary of regioneer configurations
    :return profiles: Object representation of the location hints specified in the configuration file
    """

    profiles = []
    print("Config: {}".format(conf))

    if len(conf['profiles']) < 1:
        _log.info("No profiles found for configuration file!")
        return []

    for name, config in conf.items():

        _log.info("Name: {}, config: {}".format(name, config))

        # Setup a blank profile
        hints = config['hints']
        executable = config['excecutable']
        profile = Profile(name, executable, hints=[])

        for hint in hints:
            location_hint = HintFactory.factory(hint[constants.HINT_TYPE], hint)
            profile.add_hint(location_hint)

        profiles.append(profile)

    return profiles


class Profile(object):
    """ Profile object that stores the configuration settings for a given regioneer profile. """

    def __init__(self, name, executable=None, hints=None, uuid=None):
        """ Initialize """
        self._name = name
        self._executable = executable
        self._hints = hints or []
        self._uuid = uuid

    @property
    def uuid(self):
        return self._uuid

    @property
    def executable(self):
        """ Return the command line to execute """
        return self._executable

    @executable.setter
    def executable(self, _executable):
        self._executable = _executable

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
        print("{}: There is {} hint(s) associated with this profile".format(self.name, len(self.hints)))
        for hint in self.hints:
            if hint.is_location():
                return True

        print("Regioneer determined '{}' isn't the correct profile based on hints".format(self.name))
        return False


class ProfileManager(Borg):
    """ Establish a singleton to handle all of the profiles. """

    def __init__(self):
        super(ProfileManager, self).__init__()
        self._profiles = {}

    def get_profile(self, uuid):
        """
        Retrieval of profile given the uuid.

        Args:
            uuid: the uuid of the profile to retrieve

        Returns:
            obj: a (Profile) object corresponding to the UUID
        """
        return self._profiles[uuid]

    @property
    def profiles(self):
        """
        Returns:
            All the profiles sorted based on profile name
        """

        # If sorted by UUID
        # return [val for (key, val) in sorted(self._profiles.items())]

        # Return sorting based on profile name
        return sorted(self._profiles, key=self._profiles.__get_item__)

    def load_profiles(self, profiles):
        """ TODO: Iterate over the profiles and add to the Profile Manager """

    def add_empty_profile(self, name):
        """
        Add a new profile to the list

        Args:
            name: The name of the profile
        Returns:
            UUID: The uuid of the profile in the profile manager
        """

        # Create a new profile with the provided name, and UUID
        profile_uuid = uuid.uuid1()
        _profile = Profile(name, None, None, uuid=profile_uuid)

        # Now keep track of the profile and it's uuid in the singleton
        self._profiles[profile_uuid] = _profile

    def add_profile(self, profile):
        """
        Add an already instantiated profile to the list

        Args:
            profile: The profile to add to the ProfileManager

        Returns:
            uuid: the uuid of the profile as the ProfileManager understands it
        """

        # Create a new profile with the provided name, and UUID
        profile_uuid = uuid.uuid1()

        # Set the UUID to show that the profile has been 'registered'
        profile.uuid = profile_uuid

        # Now keep track of the profile and it's uuid in the singleton
        self._profiles[profile_uuid] = profile


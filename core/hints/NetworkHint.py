# coding: utf-8
"""
    core.hints.NetworkHint
    ~~~~~~~~~~~~~

    A NetworkHint is subclass of the LocationHint object.

    Requirements: wifi / ethernet

        Ethernet Requirements:
            device
            (optional) pingable resource (public/private)
            (optional) IP address

        WiFi Requirements:
            device
            connected ssid
            (optional) surrounding ssids (threshold of +/- existing networks)
            (optional) IP address

    Todo:
        is_location: For now we should only need to implement the network_check, there maybe more checks not related
                     to networking that could go here.

        get_connected_ssid: There needs to be an abstraction as to which utilities are used to query for the ssid

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: Apache 2.0, see LICENSE for more details
"""

import re

from abc import abstractmethod

from core.hints import constants, errors
from core.hints.abstractions import LocationHint
from core.utils import networking

from subprocess import check_output


class NetworkHint(LocationHint):
    """ This is a subclass of the LocationHint that determines a location based on network based requirements. """

    def __init__(self, hint_config=constants.NETWORK_HINT_REQS):
        super(NetworkHint, self).__init__()
        self._net_device = hint_config[constants.NET_DEVICE]
        self._device_type = hint_config[constants.DEVICE_TYPE]
        self._hint_config = hint_config

    @property
    def hint_config(self):
        """ dict: Payload of the hint """
        return self._hint_config

    @property
    def net_device(self):
        """ str: This is the /dev reference to the net device you are using. """
        return self._net_device

    @net_device.setter
    def net_device(self, _device):
        self._net_device = _device

    @abstractmethod
    def network_check(self):
        """ Abstract method that is meant to handle all checks for network hint depending on the subclasses
        requirements.

        Returns:
            True if successful, False otherwise

        """
        pass

    @abstractmethod
    def is_location(self):
        """ Issues all network related checks to determine if the location matches the hint

        Returns:
            True if successful, False otherwise

        """
        pass

    def _check_output(self, opts):
        """ Meant as  a wrapper around subprocess to make mocking easy """
        return check_output(opts).decode('utf-8')

    def check_server_existence(self, host, port):
        """ Check a public server for its existence.

         Args:
             host: A string representation of the host to be pinged
             port: An integer representation of the port that a socket should try connecting to

        Returns:

            True if successful, False otherwise

        """

        networking.ping_check(host, port)


class WifiHint(NetworkHint):
    """ Subclass of NetworkHint that applies specifically to WiFi """

    def __init__(self, hint_config=constants.WIFI_HINT_CONFIG, surrounding_ssid_threshold=.6):
        NetworkHint.__init__(self, hint_config=hint_config)
        self._hint_ssid = hint_config.get(constants.CONNECTED_SSID)
        self._hint_ssids = hint_config.get(constants.NEARBY_SSIDS)
        self._ssid_threshold = surrounding_ssid_threshold
        self.ssid = None


    # TODO: The properties here should probably pull from a configuration manager keep that in mind as you are adding properties
    @property
    def hint_ssids(self):
        """ The surrounding ssids required based on the requirements object """
        return self._hint_ssids

    @property
    def hint_ssid(self):
        """ Returns the ssid connection required for the hint """
        return self._hint_ssid

    @property
    def ssid_threshold(self):
        """ The threshold percentage to determine if you are in a specific location based on
        surrounding ssids."""
        return self._ssid_threshold

    def is_location(self):
        """ Issues all network related checks to determine if the location matches the hint

        Returns:
            True if successful, False otherwise

        """
        try:
            return self.network_check()
        except errors.SSIDNotFound:
            print("Failed to find ssid: {}".format(self.hint_ssid))
            return False
        except errors.NearbySSIDError:
            print("Failed to find nearby ssids: {}".format(self.hint_ssids))
            return False

    def valid_hint_config(self):
        """ Checks the passed in config to determine if they are valid """

        reqs = self.hint_config[constants.REQUIREMENTS]
        ops  = self.hint_config.get(constants.OPTIONAL, {})

        # If the required key or its value in the config is none then fail
        print("Checking that the following reqs are valid: {}".format(reqs.keys()))
        for key, req in reqs.items():
            if not self.hint_config.get(key):
                print("Failed on key: {}".format(key))
                return False

            # if not self.hint_config.get(req):
            #     print("Failed on req: {}".format(req))
            #     return False

        for key, req in ops.items():

            # Skip options that aren't enabled
            if not self.hint_config[key]:
                print("Option: {} not enabled, skipping req check".format(key))
                continue

            print("Option: {} enabled, checking req".format(key))

            # Looks like this is key is enabled, checking it's requirements
            if not self.hint_config.get(req):
                print("Failed on req: {}".format(req))
                return False

        return True

    def network_check(self):
        """ Run the network checks required by a WiFi Hint

        Returns:

            True if successful, False otherwise
        """

        # TODO: make a special exception for this
        if not self.valid_hint_config():
            raise errors.InvalidNetworkConfig("Failed to validate network hint")

        # Check if connected ssid is required
        # By itself a WifiHint MUST have a connected ssid, but in conjunction with another hint, say ethernet,
        # then it might not be required
        if self.hint_config.get(constants.REQUIRE_CONNECTED_SSID):
            if not self.is_location_using_ssid():
                raise errors.SSIDNotFound("Not connected to: {}".format(self.hint_ssid))

        # Check if nearby ssids are required
        if self.hint_config.get(constants.REQUIRE_NEARBY_SSIDS):
            if not self.is_location_using_nearby_ssids():
                raise errors.NearbySSIDError("Failed finding the required nearby ssids")

        return True

    def get_connected_ssid(self):
        """ Get the WiFi network id that is connected
        Returns:

            The connected network SSID
        """

        # TODO: Not a huge fan of doing this via a subprocess, can we plug into nmcli?

        ssid = "WiFi not Found"

        opts = ['nmcli', '-f', 'IN-USE,SSID,CHAN,SIGNAL', 'dev', 'wifi', 'list']
        output = self._check_output(opts)
        output = output.split('\n')

        for line in output:
            tabs = line.split()
            if tabs and tabs[1] != "SSID":
                if tabs[0] == "*":
                    ssid = tabs[1]

        return ssid

    def get_surrounding_ssids(self):
        """
        Returns: A list of the surrounding ssids
        """

        all_ssids = []

        opts = ['nmcli', '-f', 'SSID', 'dev', 'wifi', 'list']
        output = self._check_output(opts)
        output = output.split('\n')

        for line in output:
            ssid = line.strip()
            if not ssid:
                continue

            # Should be the very first element unless it's an * in which case that's the connected SSID
            ssid = ssid.split()
            if ssid[0] == '*':
                ssid = ssid[1]
            else:
                ssid = ssid[0]

            # TODO: We should record channel and signal so we can keep same-named ssids
            # within the list
            if ssid not in ["SSID", self.ssid] and ssid not in all_ssids:
                print("Adding: '{}' to list of surrounding ssids".format(ssid))
                all_ssids.append( ssid )

        return all_ssids

    def is_location_using_ssid(self):
        """ Determine if this is the location based on the connected SSID """

        return self.hint_ssid == self.get_connected_ssid()

    def is_location_using_nearby_ssids(self):
        """The calculation for determining threshold met:

            (total expected ssids - found ssids) / total expected ssids

            NOTE: the default threshold is .75 unless otherwise specified

        Returns: True if nearby/surrounding ssids reach self.ssid_threshold, False otherwise
        """

        s_ssids = self.get_surrounding_ssids()

        current_thresh = float(len(s_ssids)) / float(len(self.hint_ssids))

        return current_thresh >= self.ssid_threshold


class EthernetHint(NetworkHint):
    """ Subclass of NetworkHint that applies specifically to ethernet connectivity """

    def __init__(self, hint_config=constants.NETWORK_HINT_REQS):
        NetworkHint.__init__(self, hint_config=hint_config)
        self._hint_config = hint_config

    def network_check(self):
        """ Run the network checks required by a Ethernet Hint

        Returns:

            True if successful, False otherwise
        """


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

from regioneer.core.hints import constants
from regioneer.core.hints.abstractions import LocationHint
from regioneer.core.utils import networking

from subprocess import check_output


class NetworkHint(LocationHint):
    """ This is a subclass of the LocationHint that determines a location based on network based requirements. """

    def __init__(self, requirements=constants.NETWORK_HINT_REQS):
        LocationHint.__init__(self)
        self._net_device = requirements[constants.NET_DEVICE]
        self._device_type = requirements[constants.DEVICE_TYPE]
        self._requirements = requirements

    @property
    def requirements(self):
        """ dict: Payload of the hint """
        return self._requirements

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

    def is_location(self):
        """ Issues all network related checks to determine if the location matches the hint

        Returns:
            True if successful, False otherwise

        """

        return self.network_check()

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

    def __init__(self, requirements=constants.NETWORK_HINT_REQS, surrounding_ssid_threshold=.6):
        NetworkHint.__init__(self, requirements=requirements)
        self._hint_ssid = requirements.get(constants.CONNECTED_SSID)
        self._hint_ssids = requirements.get(constants.SURROUNDING_SSIDS)
        self._ssid_threshold = surrounding_ssid_threshold
        self._requirements = requirements
        self.ssid = None

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

    def network_check(self):
        """ Run the network checks required by a WiFi Hint

        Returns:

            True if successful, False otherwise
        """

    def get_connected_ssid(self):
        """ Get the WiFi network id that is connected
        Returns:

            The connected network SSID
        """

        # TODO: Not a huge fan of doing this via a subprocess

        ssid = "WiFi not Found"

        opts = ['nmcli', '-f', 'IN-USE,SSID,CHAN,SIGNAL', 'dev', 'wifi', 'list']
        output = check_output(opts).decode('utf-8')
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
        output = check_output(opts).decode('utf-8')
        output = output.split('\n')

        for line in output:
            ssid = line.strip()
            if not ssid:
                continue

            # TODO: We should recored channel and signal so we can keep same-named ssids
            # within the list
            if ssid not in ["SSID", self.ssid] and ssid not in all_ssids:
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

    def __init__(self, requirements=constants.NETWORK_HINT_REQS):
        NetworkHint.__init__(self, requirements=requirements)
        self._requirements = requirements

    def network_check(self):
        """ Run the network checks required by a Ethernet Hint

        Returns:

            True if successful, False otherwise
        """


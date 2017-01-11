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

    def __init__(self, requirements=constants.NETWORK_HINT_REQS):
        NetworkHint.__init__(self, requirements=requirements)
        self._connected_ssid = requirements.get(constants.CONNECTED_SSID)
        self._surrounding_ssids = requirements.get(constants.SURROUNDING_SSIDS)
        self._requirements = requirements

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

        opts = ['/sbin/iwconfig', self.net_device]
        output = check_output(opts).split()

        for line in output:
            line = line.decode("utf-8")
            if "ESSID:" in line:
                ssid = line[7:-1]

        return ssid

    def get_surrounding_ssids(self):
        """

        Returns:

        """


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


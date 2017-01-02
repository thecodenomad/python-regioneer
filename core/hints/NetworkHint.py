# coding: utf-8
"""
    core.hints.NetworkHint
    ~~~~~~~~~~~~~

    A NetworkHint is subclass of the LocationHint object.

    Requirements: wifi / ethernet















    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""

from regioneer.core.hints import constants, ping_check
from regioneer.core.hints.abstractions import LocationHint

class NetworkHint(LocationHint):
    """ This is a subclass of the LocationHint object that focuses specifically on determining a location based on
    network based requirements.
    """

    def __init__(self, requirements=constants.NETWORK_HINT_REQS):
        LocationHint.__init__(self)
        self._net_device = requirements[constants.NET_DEVICE]
        self._device_type = requirements[constants.DEVICE_TYPE]
        self._connected_ssid = requirements[constants.CONNECTED_SSID]
        self._surroundsing_ssids = requirements[constants.SURROUNDING_SSIDS]
        self._requirements = requirements

    @property
    def requirements(self):
        """ Payload of the hint """
        return self._requirements

    @property
    def net_device(self):
        """ The device to use referenced based on /dev/<object> """
        return self._net_device

    @net_device.setter
    def net_device(self, _device):
        """ Set the device for this hint """
        self._net_device = _device

    def ethernet_check(self, device):
        """ Check ethernet """
        # Need to check to see if the device 

    def wifi_check(self, device):
        """ Check wifi """

    def check_server_existence(self, server, port):
        """ Check a public server for its existence """

    def is_location(self):
        """ Abstract method that should be implemented in all subclasses, erroring out if not available """
        pass
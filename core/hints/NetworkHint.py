# coding: utf-8
"""
    core.hints.NetworkHint
    ~~~~~~~~~~~~~

    A NetworkHint is subclass of the LocationHint object.

    Requirements: wifi / ethernet

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""

from regioneer.core.hints import LocationHint
from regioneer.core.hints import constants


class NetworkHint(LocationHint):
    """ This is a subclass of the LocationHint object that focuses specifically on determining a location based on
    network based requirements.
    """

    def __init__(self, payload=constants.NETWORK_HINT_PAYLOAD):
        super(LocationHint, self).__init__()
        self._device = payload[constants.DEVICE]
        self._device_type = payload[constants.DEVICE_TYPE]
        self._connected_ssid = payload[constants.CONNECTED_SSID]
        self._surroundsing_ssids = payload[constants.SURROUNDING_SSIDS]

    @property
    def device(self):
        """ The device to use referenced based on /dev/<object> """
        return self._device

    @device.setter
    def device(self, _device):
        """ Set the device for this hint """
        self._device = _device



    def ethernet_check(self, device):
        """ Check ethernet """

    def wifi_check(self, device):
        """ Check wifi """

    def check_server_existence(self, server, port):
        """ Check a public server for its existence """



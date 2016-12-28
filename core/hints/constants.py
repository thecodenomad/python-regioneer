# coding: utf-8
"""
    core.hints.constants
    ~~~~~~~~~~~~~

    LocationHint specific constants

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""

DEVICE="device"
DEVICE_TYPE="device_type"
CONNECTED_SSID="connected_ssid"
SURROUNDING_SSIDS="surrounding_ssids"


NETWORK_HINT_PAYLOAD = {

    # Physical device, prefered HWID information
    DEVICE: None,

    # Ethernet / WiFi
    DEVICE_TYPE: None,

    # The network name that the computer is connected to
    CONNECTED_SSID: None,

    # The surrounding networks (ie everything != connected_ssid if it exists, else all ssids)
    SURROUNDING_SSIDS: []
}

# coding: utf-8
"""
    core.hints.constants
    ~~~~~~~~~~~~~

    LocationHint specific constants

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: Apache 2.0, see LICENSE for more details
"""

HINT_TYPE = "hint_type"
REQUIREMENTS = "requirements"
OPTIONAL = "optional"

################################################
# Define the requirements of each type of hint #
################################################

LOCALITY = 'locality'
NETWORK  = 'network'
PHYSICAL = 'physical'

##########################
# Network Hint specifics #
##########################

# /dev/<path> location
NET_DEVICE="device"

# Valid network device types: [eth, network]
DEVICE_TYPE="device_type"

NETWORK_HINT_REQS = {

    # Physical device, prefered HWID information
    NET_DEVICE: None,

    # Ethernet / WiFi
    DEVICE_TYPE: None

}

# SSID specific constats
CONNECTED_SSID="connected_ssid"
NEARBY_SSIDS= "nearby_ssids"
REQUIRE_NEARBY_SSIDS="require_nearby_ssids"
REQUIRE_CONNECTED_SSID="require_connected_ssid"
NEARBY_SSID_THRESHOLD = "nearby_ssid_threshold"

WIFI_HINT_CONFIG = {

    REQUIREMENTS: {

        # Net device requires device type to be non null
        NET_DEVICE: DEVICE_TYPE,

        # Device type requires net device to be non null
        DEVICE_TYPE: NET_DEVICE,

        # Connected ssid requires that a net device be non null
        CONNECTED_SSID: NET_DEVICE,
    },

    # These are optional keys that allow for required options to be set
    # before they can be used. For instance, nearby ssids won't function unless
    # the computer is connected to a wifi network
    OPTIONAL: {
        # Require nearby ssids requires that nearby_ssids be a non null value,
        REQUIRE_NEARBY_SSIDS: NEARBY_SSIDS
    },

    # Physical device, prefered HWID information
    NET_DEVICE: None,

    # Ethernet / WiFi
    DEVICE_TYPE: "wifi",

    # Requirements for a Wifi Hint ('None' will result in an exception TODO: list exception)
    REQUIRE_CONNECTED_SSID: True,
    CONNECTED_SSID: None,

    NEARBY_SSID_THRESHOLD: None,

    # Optional for a Wifi Hint
    REQUIRE_NEARBY_SSIDS: False,
    NEARBY_SSIDS: None

}


###########################
# Locality Hint specifics #
###########################

GPS_COORDINATES = "gps_coords"
GPS_PROVIDER = "gps_provider"

LOCALITY_HINT_REQS = {

    # Tuple form of GPS coordinates as google would understand
    GPS_COORDINATES: None,

    # GPS provider
    GPS_PROVIDER: "geoclue"
}

###########################
# Physical Hint specifics #
###########################

ATTACHED_DEVICE = "attached_device"

PHYSICAL_HINT_REQS = {

    # Physical device, prefered HWID information
    ATTACHED_DEVICE: None,
}


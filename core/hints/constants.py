# coding: utf-8
"""
    core.hints.constants
    ~~~~~~~~~~~~~

    LocationHint specific constants

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: Apache 2.0, see LICENSE for more details
"""

HINT_TYPE = "hint_type"

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

# SSID specifics
CONNECTED_SSID="connected_ssid"
SURROUNDING_SSIDS="surrounding_ssids"

NETWORK_HINT_REQS = {

    # Physical device, prefered HWID information
    NET_DEVICE: None,

    # Ethernet / WiFi
    DEVICE_TYPE: None

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


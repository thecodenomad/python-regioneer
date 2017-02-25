# coding: utf-8
"""
    unittests.constants
    ~~~~~~~~~~~~~

    This module is meant to hold constants corresponding to unittest execution.

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: Apache 2.0, see LICENSE for more details
"""

from regioneer.core.hints.constants import NET_DEVICE, DEVICE_TYPE, NEARBY_SSIDS, CONNECTED_SSID, REQUIREMENTS, \
                                           OPTIONAL, REQUIRE_NEARBY_SSIDS


#---------------------------------#
# Required for UnitTest execution #
#---------------------------------#

OFFLINE_TEST = True

TEST_WIFI_DEVICE = "wlp1s0"

TEST_ETH_DEVICE  = "enp6s0u1u1u4"

TEST_WIFI_SSID = "pizza_is_good"

WIFI = "wifi"

ETHERNET = "ethernet"

TEST_CONNECTED_SSID = "pizza_is_good"

TEST_ETHERNET_REQS = {
    NET_DEVICE: TEST_ETH_DEVICE,
    DEVICE_TYPE: ETHERNET
}

TEST_SURROUNDING_SSIDS = [
                            'pizza_is_good', '--', 'xfinitywifi', 'JJP5', 'JJP2.4', 'Backpackers', 'Matrix',
                            'Backpackers 5G', 'myqwest239A', 'applesnseeds', 'HOME-C0B2', 'Grab-A-Sandwich',
                            'HP-Print-89-Photosmart 7520', 'HOME-4669-2.4', 'HOME-48E2', 'The Space Room',
                            'Hollyogirl', 'SweatyBalls1', 'HOME-4669-5', 'NTGR_VMB_1406851592', 'denver',
                            'lil smitty', 'HOME-5532', 'HOME-5511-5', 'cohome5', 'Shepdog1'
                         ]

TEST_WIFI_REQS = {

    REQUIREMENTS: {
        NET_DEVICE: DEVICE_TYPE,
        DEVICE_TYPE: NET_DEVICE,
        CONNECTED_SSID: NET_DEVICE,
    },

    OPTIONAL: {
        REQUIRE_NEARBY_SSIDS: NEARBY_SSIDS
    },

    NET_DEVICE: TEST_WIFI_DEVICE,
    DEVICE_TYPE: WIFI,
    CONNECTED_SSID: TEST_CONNECTED_SSID,
    NEARBY_SSIDS: TEST_SURROUNDING_SSIDS
}

TEST_NMCLI_OUTPUT =  """   pizza_is_good_slower             6     82
                        *  pizza_is_good                    44    56
                           DencoHome                        3     49
                           xfinitywifi                      1     40"""

TEST_SURROUNDING_LIST = [    'pizza_is_good_slower',
                             'pizza_is_good',
                             'DencoHome',
                             'xfinitywifi'
                        ]


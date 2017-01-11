# coding: utf-8
"""
    unittests.constants
    ~~~~~~~~~~~~~

    This module is meant to hold constants corresponding to unittest execution.

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: Apache 2.0, see LICENSE for more details
"""

from regioneer.core.hints.constants import NET_DEVICE, DEVICE_TYPE

#---------------------------------#
# Required for UnitTest execution #
#---------------------------------#

TEST_WIFI_DEVICE = "wlp1s0"

TEST_ETH_DEVICE  = "enp6s0u1u1u4"

TEST_WIFI_SSID = "pizza_is_good"

WIFI = "wifi"

ETHERNET = "ethernet"

TEST_WIFI_REQS = {
    NET_DEVICE: TEST_WIFI_DEVICE,
    DEVICE_TYPE: WIFI
}

TEST_ETHERNET_REQS = {
    NET_DEVICE: TEST_ETH_DEVICE,
    DEVICE_TYPE: ETHERNET
}


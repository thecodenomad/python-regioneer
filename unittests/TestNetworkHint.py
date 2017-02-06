""" The purpose of this module is to test the NetworkHint object """

# import pytest
from unittest.mock import patch, MagicMock, PropertyMock

import unittest
import pytest

from regioneer.core.hints import HintFactory, constants, errors
from regioneer.core.hints.LocalityHint import LocalityHint
from regioneer.core.hints.NetworkHint import NetworkHint, WifiHint, EthernetHint
from regioneer.core.hints.PhysicalHint import PhysicalHint

from regioneer.unittests.constants import TEST_WIFI_REQS, TEST_ETHERNET_REQS, TEST_WIFI_SSID, \
                                          TEST_SURROUNDING_SSIDS, TEST_CONNECTED_SSID, OFFLINE_TEST, \
                                          TEST_WIFI_DEVICE, TEST_ETH_DEVICE, WIFI, ETHERNET


class TestLocationHint(unittest.TestCase):
    """ Test the NetworkHint object"""

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_hint_factory(self):
        """ This testcase is meant to test the HintFactory class to make sure it is instantiating
        the corrgect classes. """

        network_hint  = HintFactory.factory(constants.NETWORK, constants.NETWORK_HINT_REQS)
        locality_hint = HintFactory.factory(constants.LOCALITY, constants.LOCALITY_HINT_REQS)
        physical_hint = HintFactory.factory(constants.PHYSICAL, constants.PHYSICAL_HINT_REQS)

        assert isinstance(network_hint, NetworkHint)
        assert isinstance(locality_hint, LocalityHint)
        assert isinstance(physical_hint, PhysicalHint)


class TestWiFiHint(unittest.TestCase):
    """ Test the subclassed WiFiHint """

    def test_get_device(self):
        """ Get the network device """

        # Test Retrieval
        wifi_hint = WifiHint(hint_config=TEST_WIFI_REQS)
        self.assertTrue(wifi_hint.net_device == "wlp1s0")

        # Test Setting and Retrieval
        wifi_hint.net_device = "eth0"
        self.assertTrue(wifi_hint.net_device == "eth0")

    def test_get_ssid(self):
        """" Test getting the ssid for a given device. """

        wifi_hint = WifiHint(hint_config=TEST_WIFI_REQS)

        # Make this test offline capable
        if OFFLINE_TEST:
            wifi_hint.get_connected_ssid = MagicMock()
            wifi_hint.get_connected_ssid.return_value = TEST_CONNECTED_SSID

        ssid = wifi_hint.get_connected_ssid()

        print("Method gives: {}".format(ssid))
        print("Constant gives: {}".format(TEST_WIFI_SSID))

        self.assertTrue( ssid == TEST_WIFI_SSID )

    def test_get_surround_ssids(self):
        """ Test getting the surrounding ssids """

        wifi_hint = WifiHint(hint_config=TEST_WIFI_REQS)

        if OFFLINE_TEST:
            wifi_hint.get_surrounding_ssids = MagicMock()
            wifi_hint.get_surrounding_ssids.return_value = TEST_SURROUNDING_SSIDS

        self.assertTrue(wifi_hint.is_location_using_nearby_ssids())

    def test_ssid_passing_threshold(self):
        """ Test the 'sunny-day' threshold for surrounding ssids """

        wifi_hint = WifiHint(hint_config=TEST_WIFI_REQS)
        wifi_hint.get_surrounding_ssids = MagicMock()
        wifi_hint.get_surrounding_ssids.return_value = TEST_SURROUNDING_SSIDS

        # Test 100%
        self.assertTrue(wifi_hint.is_location_using_nearby_ssids())

        half_thresh = .5
        wifi_hint = WifiHint(hint_config=TEST_WIFI_REQS, surrounding_ssid_threshold=half_thresh)
        wifi_hint.get_surrounding_ssids = MagicMock()

        subset_len = int(half_thresh * len(TEST_SURROUNDING_SSIDS))
        t_s_ssids  = TEST_SURROUNDING_SSIDS[0:subset_len]

        wifi_hint.get_surrounding_ssids.return_value = t_s_ssids

        print("Subset Length: {}, Test ssids: {}".format(subset_len, t_s_ssids))

        # Test non-default thresholds pass
        self.assertTrue(wifi_hint.is_location_using_nearby_ssids())

    def test_ssid_failing_threshold(self):
        """ Test the 'rainy-day' threshold for surrounding ssids """

        wifi_hint = WifiHint(hint_config=TEST_WIFI_REQS)
        wifi_hint.get_surrounding_ssids = MagicMock()

        # Test 0%
        wifi_hint.get_surrounding_ssids.return_value = []
        self.assertFalse(wifi_hint.is_location_using_nearby_ssids())

        # Test non-default threshold fail
        thresh = .8
        half_thresh = .5
        wifi_hint = WifiHint(hint_config=TEST_WIFI_REQS, surrounding_ssid_threshold=thresh)
        wifi_hint.get_surrounding_ssids = MagicMock()

        # Slice based on threshold
        subset_len = int(half_thresh * len(TEST_SURROUNDING_SSIDS))
        t_s_ssids  = TEST_SURROUNDING_SSIDS[0:subset_len]

        print("Subset Length: {}, Test ssids: {}".format(subset_len, t_s_ssids))
        wifi_hint.get_surrounding_ssids.return_value = t_s_ssids
        self.assertFalse(wifi_hint.is_location_using_nearby_ssids())

    def test_connected_ssid(self):
        """ Test location based on connected ssid """

        # Test passing case
        wifi_hint = WifiHint(hint_config=TEST_WIFI_REQS)
        wifi_hint._hint_ssid = TEST_CONNECTED_SSID

        # Make this test offline capable
        if OFFLINE_TEST:
            wifi_hint.get_connected_ssid = MagicMock()
            wifi_hint.get_connected_ssid.return_value = TEST_CONNECTED_SSID

        self.assertTrue(wifi_hint.is_location_using_ssid())

        # Test Failure case
        wifi_hint._hint_ssid = "--!BEEFCAKE!--"
        self.assertFalse(wifi_hint.is_location_using_ssid())


    # TODO:
    # Need to create unittests to test whether computer is in a given location for wifi settings
    # Connected SSID is required

    def test_hint_config(self):
        """ Test if in the right locatoin based on the connected ssid """

        wifi_hint_config = {
            constants.REQUIREMENTS: {
                constants.NET_DEVICE: constants.DEVICE_TYPE,
                constants.DEVICE_TYPE: constants.NET_DEVICE,
                constants.CONNECTED_SSID: constants.NET_DEVICE,
            },

            constants.OPTIONAL: {
                constants.REQUIRE_NEARBY_SSIDS: constants.NEARBY_SSIDS
            },

            constants.NET_DEVICE: TEST_WIFI_DEVICE,
            constants.DEVICE_TYPE: WIFI,
            constants.REQUIRE_CONNECTED_SSID: True,
            constants.CONNECTED_SSID: TEST_WIFI_SSID,
            constants.REQUIRE_NEARBY_SSIDS: False
        }

        # Test Valid config with just a connected SSID
        wifi_hint = WifiHint(hint_config=wifi_hint_config)
        self.assertTrue(wifi_hint.valid_hint_config())

        # Test Valid config with connected ssid and required nearby ssids
        wifi_hint_config[constants.REQUIRE_NEARBY_SSIDS] = True
        wifi_hint_config[constants.NEARBY_SSIDS] = TEST_SURROUNDING_SSIDS
        wifi_hint = WifiHint(hint_config=wifi_hint_config)
        self.assertTrue(wifi_hint.valid_hint_config())

        # Test Invalid config with connected ssid and require nearby ssids with
        # specifying nearby ssids
        wifi_hint_config[constants.REQUIRE_NEARBY_SSIDS] = True
        wifi_hint_config[constants.NEARBY_SSIDS] = []
        wifi_hint = WifiHint(hint_config=wifi_hint_config)
        self.assertFalse(wifi_hint.valid_hint_config())


    def test_is_location_connected_ssid(self):
        """ Test if in the right locatoin based on the connected ssid """

        wifi_hint_config = {
            constants.REQUIREMENTS: {
                constants.NET_DEVICE: constants.DEVICE_TYPE,
                constants.DEVICE_TYPE: constants.NET_DEVICE,
                constants.CONNECTED_SSID: constants.NET_DEVICE,
            },

            constants.OPTIONAL: {
                constants.REQUIRE_NEARBY_SSIDS: constants.NEARBY_SSIDS
            },

            constants.NET_DEVICE: TEST_WIFI_DEVICE,
            constants.DEVICE_TYPE: WIFI,
            constants.REQUIRE_CONNECTED_SSID: True,
            constants.CONNECTED_SSID: TEST_WIFI_SSID,
            constants.REQUIRE_NEARBY_SSIDS: False
        }

        wifi_hint = WifiHint(hint_config=wifi_hint_config)

        if OFFLINE_TEST:
            wifi_hint.get_connected_ssid = MagicMock()
            wifi_hint.get_connected_ssid.return_value = TEST_CONNECTED_SSID

        self.assertTrue(wifi_hint.valid_hint_config())
        self.assertTrue(wifi_hint.is_location_using_ssid())


    def test_is_location_nearby_ssids(self):
        """ Test if in the right location based on the nearby ssids and no connected ssid """

        wifi_hint_config = {
            constants.REQUIREMENTS: {
                constants.NET_DEVICE: constants.DEVICE_TYPE,
                constants.DEVICE_TYPE: constants.NET_DEVICE,
                constants.CONNECTED_SSID: constants.NET_DEVICE,
            },

            constants.OPTIONAL: {
                constants.REQUIRE_NEARBY_SSIDS: constants.NEARBY_SSIDS
            },

            constants.NET_DEVICE: TEST_WIFI_DEVICE,
            constants.DEVICE_TYPE: WIFI,
            constants.REQUIRE_CONNECTED_SSID: True,
            constants.CONNECTED_SSID: TEST_WIFI_SSID,
            constants.REQUIRE_NEARBY_SSIDS: True,
            constants.NEARBY_SSIDS: TEST_SURROUNDING_SSIDS
        }

        wifi_hint = WifiHint(hint_config=wifi_hint_config)

        if OFFLINE_TEST:
            wifi_hint.get_connected_ssid = MagicMock()
            wifi_hint.get_surrounding_ssids = MagicMock()
            wifi_hint.get_connected_ssid.return_value = TEST_CONNECTED_SSID
            wifi_hint.get_surrounding_ssids.return_value = TEST_SURROUNDING_SSIDS

        self.assertTrue(wifi_hint.valid_hint_config())
        self.assertTrue(wifi_hint.is_location_using_nearby_ssids())

    def test_network_check(self):
        """ Test the network check method """

        wifi_hint_config = {
            constants.REQUIREMENTS: {
                constants.NET_DEVICE: constants.DEVICE_TYPE,
                constants.DEVICE_TYPE: constants.NET_DEVICE,
                constants.CONNECTED_SSID: constants.NET_DEVICE,
            },

            constants.OPTIONAL: {
                constants.REQUIRE_NEARBY_SSIDS: constants.NEARBY_SSIDS
            },

            constants.NET_DEVICE: TEST_WIFI_DEVICE,
            constants.DEVICE_TYPE: WIFI,
            constants.REQUIRE_CONNECTED_SSID: True,
            constants.CONNECTED_SSID: TEST_WIFI_SSID,
            constants.REQUIRE_NEARBY_SSIDS: True,
            constants.NEARBY_SSIDS: TEST_SURROUNDING_SSIDS
        }

        # Test Retrieval
        wifi_hint = WifiHint(hint_config=wifi_hint_config)

        if OFFLINE_TEST:
            wifi_hint.is_location_using_ssid = MagicMock()
            wifi_hint.is_location_using_ssid.return_value = True
            wifi_hint.is_location_using_nearby_ssids = MagicMock()
            wifi_hint.is_location_using_nearby_ssids.return_value = True

        self.assertTrue(wifi_hint.network_check())

        # Test error scenario
        wifi_hint.valid_hint_config = MagicMock()
        wifi_hint.valid_hint_config.return_value = False

        with pytest.raises(errors.InvalidNetworkConfig):
            wifi_hint.network_check()

        wifi_hint.valid_hint_config.return_value = True
        wifi_hint.is_location_using_ssid.return_value = False
        with pytest.raises(errors.SSIDNotFound):
            wifi_hint.network_check()

        wifi_hint.is_location_using_ssid.return_value = True
        wifi_hint.is_location_using_nearby_ssids.return_value = False
        with pytest.raises(errors.NearbySSIDError):
            wifi_hint.network_check()


class TestEthernetHint(unittest.TestCase):
    """ Test teh subclassed EthernetHint """

    def test_network_check(self):
        """ Test the implementation of the NetworkHint abstract method """


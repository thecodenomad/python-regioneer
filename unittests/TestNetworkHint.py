""" The purpose of this module is to test the NetworkHint object """

# import pytest
from unittest.mock import MagicMock

import unittest

from regioneer.core.hints import HintFactory, constants
from regioneer.core.hints.LocalityHint import LocalityHint
from regioneer.core.hints.NetworkHint import NetworkHint, WifiHint, EthernetHint
from regioneer.core.hints.PhysicalHint import PhysicalHint

from regioneer.unittests.constants import TEST_WIFI_REQS, TEST_ETHERNET_REQS, TEST_WIFI_SSID, \
                                          TEST_SURROUNDING_SSIDS


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

    def test_get_ssid(self):
        """" Test getting the ssid for a given device. """

        wifi_hint = WifiHint(requirements=TEST_WIFI_REQS)
        ssid = wifi_hint.get_connected_ssid()

        print("Method gives: {}".format(ssid))
        print("Constant gives: {}".format(TEST_WIFI_SSID))

        self.assertTrue( ssid == TEST_WIFI_SSID )

    def test_get_surround_ssids(self):
        """ Test getting the surrounding ssids """

        wifi_hint = WifiHint(requirements=TEST_WIFI_REQS)
        self.assertTrue(wifi_hint.is_location_using_ssids())

    def test_ssid_passing_threshold(self):
        """ Test the 'sunny-day' threshold for surrounding ssids """

        wifi_hint = WifiHint(requirements=TEST_WIFI_REQS)
        wifi_hint.get_surrounding_ssids = MagicMock()
        wifi_hint.get_surrounding_ssids.return_value = TEST_SURROUNDING_SSIDS

        # Test 100%
        self.assertTrue(wifi_hint.is_location_using_ssids())

        half_thresh = .5
        wifi_hint = WifiHint(requirements=TEST_WIFI_REQS, surrounding_ssid_threshold=half_thresh)
        wifi_hint.get_surrounding_ssids = MagicMock()

        subset_len = int(half_thresh * len(TEST_SURROUNDING_SSIDS))
        t_s_ssids  = TEST_SURROUNDING_SSIDS[0:subset_len]

        wifi_hint.get_surrounding_ssids.return_value = t_s_ssids

        print("Subset Length: {}, Test ssids: {}".format(subset_len, t_s_ssids))

        # Test non-default thresholds pass
        self.assertTrue(wifi_hint.is_location_using_ssids())


    def test_ssid_failing_threshold(self):
        """ Test the 'rainy-day' threshold for surrounding ssids """

        wifi_hint = WifiHint(requirements=TEST_WIFI_REQS)
        wifi_hint.get_surrounding_ssids = MagicMock()

        # Test 0%
        wifi_hint.get_surrounding_ssids.return_value = []
        self.assertFalse(wifi_hint.is_location_using_ssids())

        # Test non-default threshold fail
        thresh = .8
        half_thresh = .5
        wifi_hint = WifiHint(requirements=TEST_WIFI_REQS, surrounding_ssid_threshold=thresh)
        wifi_hint.get_surrounding_ssids = MagicMock()

        # Slice based on threshold
        subset_len = int(half_thresh * len(TEST_SURROUNDING_SSIDS))
        t_s_ssids  = TEST_SURROUNDING_SSIDS[0:subset_len]

        print("Subset Length: {}, Test ssids: {}".format(subset_len, t_s_ssids))
        wifi_hint.get_surrounding_ssids.return_value = t_s_ssids
        self.assertFalse(wifi_hint.is_location_using_ssids())



class TestEthernetHint(unittest.TestCase):
    """ Test teh subclassed EthernetHint """

    def test_network_check(self):
        """ Test the implementation of the NetworkHint abstract method """


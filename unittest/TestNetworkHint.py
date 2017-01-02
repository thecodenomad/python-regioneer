""" The purpose of this module is to test the NetworkHint object """

# import pytest
# from unittest.mock import MagicMock

import unittest

from regioneer.core.hints import HintFactory, constants
from regioneer.core.hints.LocalityHint import LocalityHint
from regioneer.core.hints.NetworkHint import NetworkHint
from regioneer.core.hints.PhysicalHint import PhysicalHint


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



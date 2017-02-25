""" The purpose of this module is to test the helper functions listed in the regioneer.core.hints.__init__ """


import unittest
from unittest.mock import MagicMock, patch

# Regioneer imports
from regioneer.core.utils.networking import ping_check

PUBLIC_HOST = "www.google.com"
PRIVATE_HOST = "192.168.10.1"
SSH_HOST = "0.0.0.0"


class TestUtils(unittest.TestCase):
    """ Test the NetworkHint object"""

    def setup(self):
        pass

    def teardown(self):
        pass

    @patch('subprocess.call')
    def test_ping_check(self, mock_subprocess_call):
        """ Test the ping check helper function """

        # Make sure we handle the happy path
        mock_subprocess_call.return_value = 0

        # Dummy Host
        host = "dummyhost.domain.com"
        assert ping_check(host)

        # Make sure we handle the un-happy path
        mock_subprocess_call.return_value = 1
        assert ping_check(host) == False

    def test_ping_check_local(self):
        """ Test the ping check on actual server resources """

        assert ping_check(PUBLIC_HOST)
        assert ping_check(PRIVATE_HOST)
        assert ping_check(SSH_HOST, port=22)

        with self.assertRaises(TypeError):
            ping_check(SSH_HOST, port="stuff")



# coding: utf-8
"""
    core.hints.errors
    ~~~~~~~~~~~~~

    This module is meant to house the exceptions that a LocationHint can throw during the process of determining
    the correct location

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: Apache 2.0, see LICENSE for more details
"""


class NetworkHintError(Exception):
    """ Exception to throw when a host is not found """
    pass

class InvalidNetworkConfig(NetworkHintError):
    """ Exception to throw when hint_config is invalid """
    pass

class SSIDNotFound(NetworkHintError):
    """ Exception to throw when an SSID doesn't exist """
    pass

class NearbySSIDError(NetworkHintError):
    """ Exception to throw when a threshold is not met """
    pass

class HostNotFound(NetworkHintError):
    """ Exception to throw when a host is not found """
    pass

class ThresholdError(NetworkHintError):
    """ Exception to throw when a threshold is not met """
    pass


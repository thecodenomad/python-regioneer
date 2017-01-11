# coding: utf-8
"""
    core.hints.errors
    ~~~~~~~~~~~~~

    This module is meant to house the exceptions that a LocationHint can throw during the process of determining
    the correct location

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: Apache 2.0, see LICENSE for more details
"""


class SSIDNotFound(Exception):
    """ Exception to throw when an SSID doesn't exist """
    pass


class HostNotFound(Exception):
    """ Exception to throw when a host is not found """
    pass
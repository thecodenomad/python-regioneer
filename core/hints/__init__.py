# coding: utf-8
"""
    core.hints
    ~~~~~~~~~~~~~

    A LocationHint is an abstract representation of something that is contained within a location.

    Use Case: LAB X location maybe the only location to have access to System X (pingable or not)

    A LocationHint must have a type:    [ Locality, Network, Physical ]

    Locality:
        requires: Geoclue

    Network: A network location that is pingable for a specified fqdn or ip and port
        requires: net_device
        requires: device_type: <eth|wifi>

    Physical: Refers to an attached device, located via hwconfig
        requires: hwid

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""

from socket import socket

from regioneer.core.hints import constants

from regioneer.core.hints.LocalityHint import LocalityHint
from regioneer.core.hints.NetworkHint import NetworkHint
from regioneer.core.hints.PhysicalHint import PhysicalHint


class HintFactory(object):
    """ This is the abstract LocationHint object that is meant only as an interface """

    def factory(hint_type, requirements):
        """ Determine which type of hint we need instantiated """
        if hint_type == constants.LOCALITY:
            return LocalityHint(requirements)
        if hint_type == constants.NETWORK:
            return NetworkHint(requirements)
        if hint_type == constants.PHYSICAL:
            return PhysicalHint(requirements)

    factory = staticmethod(factory)

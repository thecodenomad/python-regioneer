#!/usr/bin/env python
# coding: utf-8
"""
    core.LocationHint
    ~~~~~~~~~~~~~

    A LocationHint is an abstract representation of something that is contained within a location.

    Use Case: LAB X location maybe the only location to have access to System X (pingable or not)

    A LocationHint must have a type:    [ Locality, Network, Physical ]

    Locality:
        requires: Geoclue

    Network: A network location that is pingable for a specified fqdn or ip and port
        requires: device
        requires: device_type: <eth|wifi>

    Physical: Refers to an attached device, located via hwconfig
        requires: hwid

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""

class LocationHint(object):
    """ This is the abstract LocationHint object that is meant only as an interface """
    pass


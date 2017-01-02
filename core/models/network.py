""" This module contains the network objects that are represented in a hint """

from abc import abstractmethod, abstractproperty

import pywifi
import netifaces

# Ignore 'Home' IPv4 and IPv6
BLACKLISTED_IPS = ["127.0.0.1", "0.0.0.0", "0:0:0:0:0:0:0:1", "::1"]


def connected_devices():
    """ List the connected ethernet devices """
    interfaces = netifaces.interfaces()

    connected_interfaces = {}
    net_addrs = []

    for i in interfaces:
        print("Looking at: {}".format(i))
        addrs = netifaces.ifaddresses(i)
        for j in addrs[netifaces.AF_INET]:
            if j['addr']:
                print("Addr exists: {}".format(j['addr']))

                # Filter out non 'connected' interfaces
                net_addrs = [j['addr'] for j in addrs[netifaces.AF_INET]
                                if j['addr'] and j['addr'] not in BLACKLISTED_IPS]

            if net_addrs:
                connected_interfaces[i] = net_addrs

    return connected_interfaces


class Network(object):
    """ Abstract class to wifi and ethernet networks. """

    @abstractproperty
    def settings(self):
        """ The purpose of this property is to return the network settings that implement
        :return:
        """
        pass

    @abstractmethod
    def check(self):
        """ The purpose of this abstract method is to implement a special type of 'check' that distinguishes the
        networks in some standard way. """
        pass


class WifiNetwork(Network):
    """ Wifi Network Object"""

    def connected_ssid(self):
        """ List the connected ssid """

        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        return iface

    def surrounding_ssids(self):
        """ List the surrounding ssids """

    def check(self):
        """ Wifi Network check to see if we are using wifi """


class EthernetNetwork(Network):
    """ Ethernet Network Object """

    def primary_device(self):
        """ List the primary device """

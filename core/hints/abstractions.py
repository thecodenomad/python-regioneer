""" This module is meant to store all abstract classes requried for the hints module """

from abc import abstractmethod


class LocationHint(object):
    """ This is the abstract LocationHint object that is meant only as an interface """

    @abstractmethod
    def is_location(self):
        """ Abstract method that should be implemented in all subclasses, erroring out if not available """
        pass


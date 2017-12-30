# coding: utf-8
"""
    core.hints.PhysicalHint
    ~~~~~~~~~~~~~

    A PhysicalHint is subclass of the LocationHint object.

    Requirements: /dev/<path>

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""

from core.hints.abstractions import LocationHint


class PhysicalHint(LocationHint):
    """ This is a subclass of the LocationHint object that focuses specifically on determining a location based on
    physical locality of the user (ie GPS).
    """

    def __init__(self, requirements):
        super(PhysicalHint, self).__init__()
        self.requirements = requirements

    def is_location(self):
        """ Abstract method that should be implemented in all subclasses, erroring out if not available """
        pass


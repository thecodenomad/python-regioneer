# coding: utf-8
"""
    core.hints.LocatityHint
    ~~~~~~~~~~~~~

    A LocalityHint is subclass of the LocationHint object.

    Requirements: geoclue

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""

from regioneer.core.hints import LocationHint

class LocalityHint(LocationHint):
    """ This is a subclass of the LocationHint object that focuses specifically on determining a location based on
    physical locality of the user (ie GPS).
    """

   def __init__(self):
       super(LocationHint, self).__init__()
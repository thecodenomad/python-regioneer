#!/usr/bin/env python
# coding: utf-8
"""
    core.utils.decorators
    ~~~~~~~~~~~~~

    The purpose of this module is to define decorators for overrides specific to the internals. For instance
    a decorator to turn on or off functions based on the projects config file.

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""

def learning_enabled(func):
    def wrapper(input):

        return func(intput)
    return wrapper


# coding=utf-8
"""
Various PayPal API related exceptions.
"""

class Error(Exception):
    """
    Parent Error class. Nothing error-specific here.
    """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)


class ApiError(Error):
    """
    Used to denote some kind of generic API error.
    """
    pass

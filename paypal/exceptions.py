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


class PayPalError(Error):
    """
    Used to denote some kind of generic error.
    """
    pass


class PayPalConfigError(Error):
    """
    Raised when a configuration problem arises.
    """
    pass

class PayPalAPIResponseError(Error):
    """
    Raised when there is an error coming back with a PayPal NVP API response.
    """
    pass
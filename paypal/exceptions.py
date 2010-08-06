# coding=utf-8
"""
Various PayPal API related exceptions.
"""

class PayPalError(Exception):
    """
    Used to denote some kind of generic error.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class PayPalConfigError(PayPalError):
    """
    Raised when a configuration problem arises.
    """
    pass


class PayPalAPIResponseError(PayPalError):
    """
    Raised when there is an error coming back with a PayPal NVP API response.
    """
    pass
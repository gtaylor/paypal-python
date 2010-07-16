# coding=utf-8
"""
Response parsing and processing.
"""

from cgi import parse_qs

import exceptions 

class Response(object):
    """
    Parse and prepare the reponse from PayPal's API.
    """
    def __init__(self, query_string, config):
        self.raw = parse_qs(query_string)
        self.config = config

    def __str__(self):
        return str(self.raw)

    def __getattr__(self, key):
        key = key.upper()
        try:
            value = self.raw[key]
            if len(value) == 1:
                return value[0]
            return value
        except KeyError:
            if self.config.KEY_ERROR == None:
                return None
            else:
                raise AttributeError(self)

    def success(self):
        """
        Checks for the presence of errors in the response. Returns True if
        all is well, False otherwise.
        """
        return self.ack.upper() in (self.config.ACK_SUCCESS, 
                                    self.config.ACK_SUCCESS_WITH_WARNING)
    success = property(success)
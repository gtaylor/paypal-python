# coding=utf-8

from cgi import parse_qs

import exceptions 


class Response(object):


    def __init__(self , query_string , config ):
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
        return self.ack.upper() in ( self.config.ACK_SUCCESS , self.config.ACK_SUCCESS_WITH_WARNING )
    success = property(success)
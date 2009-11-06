# coding=utf-8

from cgi import parse_qs
from settings import ACK_SUCCESS, ACK_SUCCESS_WITH_WARNING

class Response(object):
    def __init__(self, query_string):
        self.raw = parse_qs(query_string)

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
            raise AttributeError(self)

    def success(self):
        return self.ack.upper() in ACK_SUCCESS, ACK_SUCCESS_WITH_WARNING
    success = property(success)
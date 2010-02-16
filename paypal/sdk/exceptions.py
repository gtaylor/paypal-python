# coding=utf-8

class Error(Exception):
    """Parent Error"""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)


class ApiError(Error):
    pass
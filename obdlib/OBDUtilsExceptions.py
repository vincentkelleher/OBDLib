# -*- coding: utf-8 -*-


class NoResponseException(ValueError):
    def __init__(self, *args):
        self.message = "There is no response or the response is empty"

        super(NoResponseException, self).__init__(*args)


class InvalidCommandResponseException(ValueError):
    def __init__(self, expected, actual, *args):
        self.message = "Wrong command response - expected " + expected + " got " + actual

        super(InvalidCommandResponseException, self).__init__(self.message, *args)


class InvalidChecksumException(ValueError):
    def __init__(self, expected, actual, *args):
        self.message = "Wrong mode response - expected " + expected + " got " + actual

        super(InvalidChecksumException, self).__init__(self.message, *args)


class InvalidResponseModeException(InvalidChecksumException):
    def __init__(self, expected, actual, *args):
        super(InvalidResponseModeException, self)


class InvalidResponsePIDException(InvalidChecksumException):
    def __init__(self, expected, actual, *args):
        super(InvalidResponsePIDException, self)
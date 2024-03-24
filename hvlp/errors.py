# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

import logger
import sys

sys.path.append(str('.'))
sys.path.append(str('..'))


class HvlpError(Exception):
    """ Base error for the application """

    def __init__(self, message, reason):
        self.message = message
        self.reason = reason
        self.separator = ":"

    def __str__(self):

        # Additional information to the base message
        if self.reason:
            result = self.message + " " + self.separator + " " + self.reason

        # Only the base message
        else:
            result = self.message

        return result


class HvlpParsingError(HvlpError):
    """ Raised when application cannot deserialize the byte stream """

    def __init__(self, reason=""):
        super(HvlpParsingError, self).__init__(
            message="The stream is empty or cannot be converted to a packet object",
            reason=reason
        )


class HvlpConnectionError(HvlpError):
    """ Raise when the TCP connection is broken """

    def __init__(self, reason=""):
        super(HvlpConnectionError, self).__init__(
            message="The client is not connected to the broker",
            reason=reason
        )


class HvlpAlreadyConnected(HvlpError):
    """ Raise when the client tries to open more than one TCP connection"""

    def __init__(self, reason=""):
        super(HvlpAlreadyConnected, self).__init__(
            message="The client is already connected to the broker",
            reason=reason
        )


class HvlpPayloadFormatError(HvlpError):
    """ Raise when a component cannot decode the payload of a message"""

    def __init__(self, reason=""):
        super(HvlpPayloadFormatError, self).__init__(
            message="The allowed values for each byte are in the range 0-255",
            reason=reason
        )


class HvlpCommandError(HvlpError):
    """ Raise when the user tries to execute an unknown command """

    def __init__(self, reason=""):
        super(HvlpCommandError, self).__init__(
            message="Unknown Command",
            reason=reason
        )


class HvlpArgumentsError(HvlpError):
    """ Raise when the command expects and argument but none is given """

    def __init__(self, reason=""):
        super(HvlpArgumentsError, self).__init__(
            message="Missing arguments",
            reason=reason
        )


if __name__ == "__main__":
    logger.configure_logger()

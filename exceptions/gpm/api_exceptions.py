class GpmMalformedTrackException(Exception):
    """
    This exception is thrown when we attempt to create a GpmTrack using a malformed track object

    Args:
        message (str): Description of the exception
    """

    def __init__(self, message: str):
        super().__init__(message)


class UnauthenticatedClientException(Exception):
    """
    This exception is thrown when we attempt to use the mobile client to perform actions that require authentication
    but the client is not authenticated

    Args:
        message (str): Description of the exception
    """

    def __init__(self, message: str):
        super().__init__(message)

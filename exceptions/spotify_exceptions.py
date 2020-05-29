class InvalidAuthTokenReceived(Exception):
    """
    This exception should be thrown when an invalid auth token has been received from the user
    """

    def __init__(self, message: str):
        super().__init__(message)


class InvalidTrackUsed(Exception):
    """
    This exception should be thrown when trying to perform an action with a Spotify track but the track object is not
    properly formed
    """
    def __init__(self, message: str):
        super().__init__(message)

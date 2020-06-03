class NoMatchException(Exception):
    """
    This exception is thrown when we fail to find a Spotify equivalent for a google play music track

    Args:
        message (str): Description of the exception
    """

    def __init__(self, message: str):
        super().__init__(message)


class SpotifyMalformedTrackException(Exception):
    """
    This exception is thrown when we attempt to create a SpotifyTrack using a malformed track object

    Args:
        message (str): Description of the exception
    """

    def __init__(self, message: str):
        super().__init__(message)

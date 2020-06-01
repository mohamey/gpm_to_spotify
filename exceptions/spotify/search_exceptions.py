class NoMatchException(Exception):
    """
    This excception is thrown when we fail to find a Spotify equivalent for a google play music track

    Args:
        message (str): Description of the exception
    """

    def __init__(self, message: str):
        super().__init__(message)

class AuthException(Exception):
    """
    This excception is thrown when we fail to authenticate the mobile client using the gmusicapi

    Args:
        message (str): Description of the exception
    """

    def __init__(self, message: str):
        super().__init__(message)

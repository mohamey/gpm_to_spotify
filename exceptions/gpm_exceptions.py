class NotAuthenticatedException(Exception):
    """
    This exception is thrown when an action on the Skyjam API is attempted but the wrapper has not yet been
    authenticated
    """

    def __init__(self, message):
        super().__init__(message)


class UnableToGetOauthCredentials(Exception):
    """
    This exception is thrown when the wrapper is unable to get the oauth token to access the Skyjam API
    """

    def __init__(self, message):
        super().__init__(message)


class UnableToLoginToService(Exception):
    """
    This exception is thrown when the wrapper is unable to login to the Skyjam API
    """

    def __init__(self, message):
        super().__init__(message)

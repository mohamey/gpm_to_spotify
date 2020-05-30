class InvalidConfigException(Exception):
    """
    This exception is thrown when there's an error parsing the config for the service

    Args:
        message (str): Description of the exception
    """

    def __init__(self, message: str):
        super().__init__(message)

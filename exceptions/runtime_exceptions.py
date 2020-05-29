class InvalidConfigException(Exception):
    """
    This exception is thrown when there's an error parsing the config for the service
    """

    def __init__(self, message):
        super().__init__(message)

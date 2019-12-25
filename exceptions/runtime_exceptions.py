# This exception should be thrown when the config is invalid
class InvalidConfigException(Exception):
    def __init__(self, message):
        super().__init__(message)
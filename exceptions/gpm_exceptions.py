"""To be used when performing an action that client requires authentication to do"""
class NotAuthenticatedException(Exception):
    def __init__(self, message):
        super().__init__(message)


"""To be used when theres been a failure trying to get oauth token"""
class UnableToGetOauthCredentials(Exception):
    def __init__(self, message):
        super().__init__(message)

"""To be used when unable to login to the service"""
class UnableToLoginToService(Exception):
    def __init__(self, message):
        super().__init__(message)

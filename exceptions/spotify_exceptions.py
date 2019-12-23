# Error should be thrown when an invalid auth token is received
class InvalidAuthTokenReceived(Exception):
   def __init__(self, message):
       super().__init__(message)
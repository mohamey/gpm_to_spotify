# Error should be thrown when an invalid auth token is received
class InvalidAuthTokenReceived(Exception):
   def __init__(self, message):
       super().__init__(message)

# Exception should be thrown when trying to perform an action with a track on Spotify but the track object isn't
# properly formed
class InvalidTrackUsed(Exception):
    def __init__(self, message):
        super().__init__(message)
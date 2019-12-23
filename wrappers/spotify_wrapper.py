from exceptions.spotify_exceptions import InvalidAuthTokenReceived
from spotipy import Spotify
import spotipy.util as util

class SpotifyWrapper:
    def __init__(self):
        self.__spotify = Spotify()
        self.__scope = 'user-library-read,user-library-modify'
        self.__client_id = 'client id here'
        self.__client_secret = 'client secret here'
        self.__redirect_url = 'http://localhost:8080/redirect'
        self.__user = 'user here'

    def handle_auth(self):
        token = util.prompt_for_user_token(self.__user, self.__scope, self.__client_id,\
            self.__client_secret, self.__redirect_url)

        if not token or len(token) == 0:
            raise InvalidAuthTokenReceived("Token is empty.")

        self.__spotify = Spotify(auth=token)

    def get_user_saved_tracks(self):
        results = self.__spotify.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(f"{track['name']} - {track['artists'][0]['name']}")

from exceptions.spotify_exceptions import InvalidAuthTokenReceived
from json import load
from spotipy import Spotify
import spotipy.util as util

class SpotifyWrapper:
    def __init__(self):
        self.__spotify = Spotify()
        self.__scope = 'user-library-read,user-library-modify'
        self.__redirect_url = 'http://localhost:8080/redirect'
        self.__load_secrets()

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

    def find_track(self, track):
        results = self.__spotify.search(q="{track} album:{album} year:{year}".format(track=track.get_title(),
                                                     album=track.get_album(), year=track.get_year()), type='track')

        print(f"Found {len(results['tracks']['items'])} results for {track.get_title()} - {track.get_artist()}")
        for result_track in results['tracks']['items']:
            print(f"{result_track['name']} - {result_track['artists'][0]['name']}")

    def __load_secrets(self):
        with open('/home/yasir/Documents/Projects/gpm_to_spotify/secrets.json') as secrets_file:
            secrets = load(secrets_file)
            self.__client_id = secrets['client']['id']
            self.__client_secret = secrets['client']['secret']
            self.__user = secrets['user']


from exceptions.spotify_exceptions import InvalidAuthTokenReceived, InvalidTrackUsed
from fuzzywuzzy import fuzz
from json import load
from meta.structures.track import Track
from spotipy import Spotify
import re
import spotipy.util as util


class SpotifyWrapper:
    def __init__(self, config):
        self.__spotify = Spotify()
        self.__scope = 'user-library-read,user-library-modify'
        self.__redirect_url = 'http://localhost:8080/redirect'
        self.__client_id = config['client']['id']
        self.__client_secret = config['client']['secret']
        self.__user = config['user']
        self.mapped_tracks = []
        self.unmapped_tracks = []

    # Handle authenticating this app with Spotify for a given user
    def handle_auth(self, token=None):
        if not token:
            token = util.prompt_for_user_token(self.__user, self.__scope, self.__client_id,\
                self.__client_secret, self.__redirect_url)

        if not token or len(token) == 0:
            raise InvalidAuthTokenReceived("Token is empty.")

        self.__spotify = Spotify(auth=token)

    # Get list of songs saved by the user
    def get_user_saved_tracks(self):
        return self.__spotify.current_user_saved_tracks()

    # Upload track to library in Spotify
    def add_saved_tracks(self, tracks=None):
        if not tracks:
            tracks = self.mapped_tracks

        # We have a uri, just use spotipy to add to saved tracks
        index = 0
        while index < len(tracks):
            chunk_size = min(index + 50, len(tracks))
            chunk = tracks[index:chunk_size]
            index = chunk_size

            self.__spotify.current_user_saved_tracks_add([track['uri'] for track in chunk])

    # Given a list of tracks, find there spotify equivalents
    def find_tracks(self, tracks):
        for track in tracks:
            self.__find_track(track)

    # Use spotify to find a track on the spotify service, goal is to retrieve a track uri
    def __find_track(self, track):
        results = self.__spotify.search(q=self.__get_query_string(track, blacklist=['year'], strip_brackets=True),
                                        type='track', limit=10)

        if len(results['tracks']['items']) == 0:  # Try again with more lax search terms
            results = self.__spotify.search(q=self.__get_query_string(track, blacklist=['album', 'artist', 'year'],
                                                                     strip_brackets=True), type='track', limit=50)

        if len(results['tracks']['items']) > 0:
            track_result_list = [self.__map_result_to_track(result) for result in results['tracks']['items']]
            scored_results = {self.__get_match_score(track, result_track):result_track for result_track in track_result_list}
            print(f"Best Matched Result for {track['title']} - {track['artist']} from Spotify is {scored_results[max(scored_results)]}")
            top_score = max(scored_results)
            if top_score > 75:
                self.mapped_tracks.append(scored_results[top_score])
            else:
                print("No matches found with a high enough score")
                self.unmapped_tracks.append(track)

        else:
            print(f"Could not find a match for {track['title']} - {track['artist']}")
            self.unmapped_tracks.append(track)

    # Load spotify config info
    def __load_secrets(self):
        with open('/home/yasir/Documents/Projects/gpm_to_spotify/secrets.json') as secrets_file:
            secrets = load(secrets_file)
            self.__client_id = secrets['client']['id']
            self.__client_secret = secrets['client']['secret']
            self.__user = secrets['user']

    # Create a formatted query string to find a track on Spotify
    def __get_query_string(self, track, blacklist=[], strip_brackets=False):
        query_parts = []
        for key, value in track.items():
            if strip_brackets:
                # Remove brackets and it's contents from the value
                value = re.sub(" ?\([^)]+\)", "", str(value))
            if key == 'title':
                query_parts.append(value)
            elif value is not None and key not in blacklist:
                query_parts.append("{searchKey}:{searchValue}".format(searchKey=key, searchValue=value))

        return ' '.join(query_parts)

    # Map Resulting Spotify track item to a local Track object
    def __map_result_to_track(self, result_track):
        return Track(title=result_track['name'],
                     artist=result_track['artists'][0]['name'],  # TODO: Verify primary artist is always first
                     album=result_track['album']['name'],
                     uri=result_track['uri'])

    # Compare two track objects, use fuzzy matching to generate a simple match score
    def __get_match_score(self, gpm_track, spotify_track):
        score = 0
        common_attributes = 0

        for key in spotify_track:
            # We only care about common Attributes
            if key in gpm_track:
                spotify_value = spotify_track[key].lower()
                gpm_value = gpm_track[key].lower()

                common_attributes += 1
                score += fuzz.partial_ratio(spotify_value, gpm_value)

        return int(score / common_attributes)



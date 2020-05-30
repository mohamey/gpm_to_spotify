from exceptions.spotify_exceptions import InvalidAuthTokenReceived, InvalidTrackUsed
from fuzzywuzzy import fuzz
from json import dumps, load
from meta.structures.track import GpmTrack, SpotifyTrack, MatchedTrack, TrackEncoder
from spotipy import Spotify
from typing import List

import logging
import re
import spotipy.util as util

logger = logging.getLogger()


class SpotifyWrapper:
    """
    This wrapper is responsible for interacting with the Spotify API to perform actions such as search and updating the
    library. It's a stateful wrapper, most methods update the instances internal state

    Attributes:
        mapped_tracks (List[SpotifyTrack]): List of tracks that were successfully matched from google play music
        unmapped_tracks (List[SpotifyTrack]): List of tracks that were not correctly matched from google play music.
        Based on match score threshold
        merged_tracks (List[MatchedTrack]): List of track pairings of google play music & Spotify
    """

    def __init__(self, config: dict):
        """
        Constructor for creating a SpotifyWrapper. Contains Spotify Client Secrets and User configuration

        Args:
            config (dict): A Dict containing config for the Spotify Wrapper

        TODO:
            * Passing in a dict makes it difficult to see whats being passed in here. Should explicitly bind arguments,
                or create a Config Object with explicitly defined properties.
        """

        self.__spotify: Spotify = Spotify()
        self.__scope: str = 'user-library-read,user-library-modify'
        self.__redirect_url: str = 'http://localhost:8080/redirect'
        self.__client_id: str = config['client']['id']
        self.__client_secret: str = config['client']['secret']
        self.__user: str = config['user']
        self.mapped_tracks: List[SpotifyTrack] = []
        self.unmapped_tracks: List[SpotifyTrack] = []
        self.merged_tracks: List[MatchedTrack] = []

    def handle_auth(self, token: str = None) -> None:
        """
        Handle application auth with Spotify. Token is optional, we can prompt user for token using this application.

        Args:
            token (str): Spotify Auth Token to be used when communicating with the spotify API

        Returns:
            None

        Raises:
            InvalidAuthTokenReceived when this method is called with an empty or null token

        """

        if not token:
            token = util.prompt_for_user_token(self.__user, self.__scope, self.__client_id,
                                               self.__client_secret, self.__redirect_url)

        if not token or len(token) == 0:
            raise InvalidAuthTokenReceived("Token is empty.")

        self.__spotify = Spotify(auth=token)

    def get_user_saved_tracks(self) -> List[dict]:
        """
        Proxy for the spotipy current_user_saved_tracks method.

        Returns:
            List[dict] of tracks in the user saved tracks

        """

        return self.__spotify.current_user_saved_tracks()

    # Upload track to library in Spotify
    def add_track_uris_to_library(self, track_uris: List[str] = None) -> None:
        """
        Add a list of track URIs to a users list of liked songs on Spotify
        Args:
            track_uris (List[str]): A list of uris to be added to the users liked songs. If this is none, a list
            of URIs will be generated from the internal attribute `mapped_tracks`.

        Returns:
            Nothing, just updates the saved tracks

        TODO:
            * Should raise an exception if a null input has been provided

        """

        if not track_uris:
            track_uris = [track['uri'] for track in self.mapped_tracks]

        # Generate a list of track uris, use spotipy to update library
        self.__update_library(track_uris)

    def __update_library(self, track_uris: List[str]) -> None:
        """
            Given a list of Track URIs, split them into sublists of 50 URIs each and submit them to Spotify to be added
            to a users list of liked songs
        Args:
            track_uris (List[str]): A List of Spotify Track URIs to be added to the users library

        Returns:
            Nothing, should just update the saved tracks on the users spotify account

        TODO:
            * Should raise an exception if null input is being provided

        """

        if not track_uris:
            logger.info("No Track URIs provided")
            return

        index = 0
        while index < len(track_uris):
            # Break the updates into chunks of 50
            slice_end_index = min(index + 50, len(track_uris))
            tracks_slice = track_uris[index:slice_end_index]
            index = slice_end_index

            self.__spotify.current_user_saved_tracks_add(tracks_slice)

    # Given a list of tracks, find there spotify equivalents
    def find_tracks(self, tracks: List[GpmTrack]) -> None:
        """
        Takes a list of GPM Tracks and attempts to match them with their equivalents in Spotify. Matching is done using
        Spotify's search functionality.
        Args:
            tracks (List[GpmTrack]): A list of GpmTracks that we want to match to Spotify Tracks

        Returns:
            None - This just updates the internal wrapper attribute `mapped_tracks`

        """

        for track in tracks:
            self.__find_track(track)

    def tracks_to_json(self) -> str:
        """
        Takes the internal `merged_tracks` attribute and converts it to a JSON String
        Returns:
            A JSON String representing `merged_tracks`

        """

        return dumps(self.merged_tracks, cls=TrackEncoder)

    def dump_tracks_to_json(self, filename):
        """
        Takes the internal `merged_tracks` attribute and dumps it to a json file specified by the filename arg

        Args:
            filename (str): File to write `merged_tracks` to. It will overwrite existing files.

        Returns:
            Nothing, just writes to file.

        """

        with open(filename, 'w') as out:
            out.write(self.tracks_to_json())

    def get_matched_tracks(self) -> str:
        """
        Wrapper for getting `merged_tracks` as JSON.

        Returns:
            JSON String representing the `merged_tracks` attribute.

        TODO:
            * Deprecate this. It's pointless.

        """

        return self.tracks_to_json()

    # Use spotify to find a track on the spotify service, goal is to retrieve a track uri
    def __find_track(self, track: GpmTrack) -> None:
        """
        This function uses Spotify's search endpoint to attempt to match the GPM Track with the Spotify Track. The
        goal is to build a SpotifyTrack object from this.

        The Search Strategy is as follows:
            1. Search Spotify using all attributes available in the GpmTrack excluding the year. Get 10 results this
                time
            2. If this returns no results, try again but this time without the album & artist as well. Get 50 results
                this time.
            3. If we've obtained results, score the accuracy of all the matches
            4.
                a. Get the highest scoring match and select it as the Spotify Track to be used. Create a new MatchedTrack
                    object and add it to the list of `mapped_tracks`.
                b. If none of the search results return a score higher than 75, assume there is no match, and add the
                    GpmTrack to the list of `unmapped_tracks`.
            5. If no results are returned from the second search, consider the GpmTrack unmatched and add it to
                `unmapped_tracks`.

        Args:
            track (GpmTrack): The GpmTrack we're trying to match to the Spotify Database

        Returns: None. Updates the internal attributes `mapped_tracks`, `merged_tracks` & `unmapped_tracks` depenending
                        on the outcome.

        TODO:
            * Stop filtering based on Threshold, let the client handle this. Should just return each track with it's
                best match and allow the client to make the decision.

        """

        results = self.__spotify.search(q=self.__get_query_string(track, blacklist=['year'], strip_brackets=True),
                                        type='track', limit=10)

        if len(results['tracks']['items']) == 0:  # Try again with more lax search terms
            results = self.__spotify.search(q=self.__get_query_string(track, blacklist=['album', 'artist', 'year'],
                                                                      strip_brackets=True), type='track', limit=50)

        if len(results['tracks']['items']) > 0:
            track_result_list = [self.__map_result_to_track(result) for result in results['tracks']['items']]
            scored_results = {self.__get_match_score(track, result_track): result_track for result_track in
                              track_result_list}
            print(f"Best Matched Result for {track['title']} - {track['artist']} from Spotify is \
                    {scored_results[max(scored_results)]}")
            top_score = max(scored_results)
            if top_score > 75:
                best_matched_track = scored_results[top_score]
                self.mapped_tracks.append(best_matched_track)
                self.merged_tracks.append(MatchedTrack(
                    gpm=track,
                    spotify=best_matched_track
                ))
            else:
                print("No matches found with a high enough score")
                self.unmapped_tracks.append(track)

        else:
            print(f"Could not find a match for {track['title']} - {track['artist']}")
            self.unmapped_tracks.append(track)
            self.merged_tracks.append(MatchedTrack(
                gpm=track,
                spotify=None
            ))

    def __load_secrets(self) -> None:
        """
        Load Spotify API Secrets into the Wrapper

        Returns: None, this should just update internal attributes

        """

        with open('/home/yasir/Documents/Projects/gpm_to_spotify/secrets.json') as secrets_file:
            secrets = load(secrets_file)
            self.__client_id = secrets['client']['id']
            self.__client_secret = secrets['client']['secret']
            self.__user = secrets['user']

    @staticmethod
    def __get_query_string(track: GpmTrack, blacklist: List[str] = (), strip_brackets: bool = False) -> str:
        """
        This method should create a valid query string to be used with the spotipy search function

        Args:
            track (GpmTrack): The GpmTrack we are searching Spotify for
            blacklist (List[str]): List of keys from the GPM Track we should remove from the search criteria
            strip_brackets (bool): Whether we should strip any brackets that occur in any of the GpmTrack attributes

        Returns:
            A valid query string to be used when searching Spotify

        TODO:
            * Get rid of the regex, its a performance hog.
        """

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

    @staticmethod
    def __map_result_to_track(result_track: dict) -> SpotifyTrack:
        """
        Map a response dict from Spotify to a SpotifyTrack Object

        Args:
            result_track (dict): A Dict representing a track from Spotify.

        Returns:
            A new SpotifyTrack object containing only the info we care about

        TODO:
            * Add an album art link to the SpotifyTrack Object

        """

        return SpotifyTrack(title=result_track['name'],
                            artist=result_track['artists'][0]['name'],  # TODO: Verify primary artist is always first
                            album=result_track['album']['name'],
                            uri=result_track['uri'])

    # Compare two track objects, use fuzzy matching to generate a simple match score
    @staticmethod
    def __get_match_score(gpm_track: GpmTrack, spotify_track: SpotifyTrack) -> int:
        """
        Compare a GPM Track with a Spotify Track to assess how likely they are to be a match. Matching done using
        Fuzzy matching.

        Args:
            gpm_track (GpmTrack): The GPM Track we're trying to migrate
            spotify_track (SpotifyTrack): The potential spotify match returned from the search

        Returns:
            score (int): A Score indicating how likely the two tracks are a match

        TODO:
            * Improve matching, a lot of live tracks are being used in lieu of the correct studio version. A lot of
                remixes are also being incorrectly used. Maybe perform some normalisation?
        """

        score = 0
        common_attributes = 0

        for key in spotify_track:
            # We only care about common Attributes dictated by the GPM Track
            if key in gpm_track:
                spotify_value = spotify_track[key].lower()
                gpm_value = gpm_track[key].lower()

                common_attributes += 1
                score += fuzz.partial_ratio(spotify_value, gpm_value)

        return int(score / common_attributes)

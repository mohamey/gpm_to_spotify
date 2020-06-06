from exceptions.spotify.search_exceptions import NoMatchException
from fuzzywuzzy import fuzz
from meta.structures.track import GpmTrack, SpotifyTrack
from spotipy import Spotify
from typing import Tuple


class SearchWrapper:
    """
    This class is responsible for interfacing with the Search Service. It should map google play music tracks to spotify
    tracks.
    """

    @staticmethod
    def get_spotify_match(spotify_client: Spotify, gpm_track: GpmTrack) -> SpotifyTrack:
        """
        This function takes a spotify client & gpm track and returns it's Spotify Equivalent

        Args:
            spotify_client (Spotify): An authenticated Spotify Client
            gpm_track (GpmTrack): A GpmTrack object to search for on Spotify

        Returns:
            SpotifyTrack: A SpotifyTrack object representing the Spotify equivalent of the GpmTrack supplied

        Raises:
            NoMatchException: When no match is found for the track, raise an exception

        Todo:
            Have the search prefer explicit tracks

        """

        # Convert GPM Track To Search String
        search_string: str = SearchWrapper.__get_search_query(gpm_track=gpm_track)

        # Search Spotify API using all available criteria
        search_results: dict = (spotify_client.search(q=search_string, type='track', limit=50))['tracks']

        # If we didn't get any results, relax the critetia and search again
        if search_results['total'] == 0:
            search_string: str = SearchWrapper.__get_search_query(gpm_track=gpm_track, attributes_filter=('album','artist'))
            search_results: dict = spotify_client.search(q=search_string, type='track', limit=50)['tracks']

            if search_results['total'] == 0:
                # Give up, we still dont have any matches
                raise NoMatchException(f"No match for {gpm_track.get_title()} - {gpm_track.get_artist()} - {gpm_track.get_album()} - {search_string}")

        # We have results, parse the items
        search_results = search_results['items']

        # Set the best result to a placeholder with an impossible score
        best_result: SpotifyTrack = SpotifyTrack(title='Placeholder', artist='Placeholder', uri='test', score=-1)
        for result in search_results:
            current_result: SpotifyTrack = SearchWrapper.__parse_result_to_track(result)
            result_score: int = SearchWrapper.__score_match(gpm_track=gpm_track, spotify_track=current_result)

            current_result.set_score(score=result_score)

            best_result = max(best_result, current_result, key=lambda x: x.get_score())

        return best_result

    @staticmethod
    def __get_search_query(gpm_track: GpmTrack, attributes_filter: Tuple[str] = ()) -> str:
        """
        Given a GPM Track, encode a spotify search string
        Args:
            gpm_track (GpmTrack): -> GpmTrack we're searching Spotify for
            attributes_filter (Tuple[str]): A Tuple of GpmTrack Attributes to ignore in the search

        Returns:
            str: A Spotify Search String

        Todo:
            * Raise an exception when the resulting search string is empty

        """

        query_parts = []
        if 'title' not in attributes_filter:
            title_value: str = gpm_track.get_title()

            if title_value is not None:
                query_parts.append(f"track:\"{title_value}\"")

        if 'artist' not in attributes_filter:
            artist_value: str = gpm_track.get_artist()

            if artist_value is not None:
                query_parts.append(f"artist:\"{artist_value}\"")

        if 'album' not in attributes_filter:
            album_value: str = gpm_track.get_album()

            if album_value is not None:
                query_parts.append(f"album:\"{album_value}\"")

        return '+'.join(query_parts)

    @staticmethod
    def __parse_result_to_track(result: dict) -> SpotifyTrack:
        """
        This method should parse a single track result from the Spotify API into a SpotifyTrack object

        Args:
            result (dict): A Dict representing a track search result from the Spotify API

        Returns:
            SpotifyTrack: A new Spotify Track representing the search result from Spotify

        Raises:
            SpotifyMalformedTrackException: Raised by the SpotifyTrack when the result we're trying to parse into the Spotify
                Track object doesn't meet the constructor's requirements

        """

        return SpotifyTrack(
            title=result['name'],
            artist=result['artists'][0]['name'],
            album=result['album']['name'],
            album_art_url=result['album']['images'],
            uri=result['uri'],
            year=result['album']['release_date'][0:4]
        )

    @staticmethod
    def __score_match(gpm_track: GpmTrack, spotify_track: SpotifyTrack) -> int:
        """
        Using the gpm_track as the reference object, get each of the gpm track's attributes and compare it with the
        spotify track using fuzzy matching, then get the average score for each attribute.

        Args:
            gpm_track (GpmTrack): gpm track we want to compare
            spotify_track (SpotifyTrack): Spotify Track we want to compare

        Returns:
            int: Score for the match

        """

        score, common_attributes = 0, 0

        gpm_dict: dict = vars(gpm_track)
        spotify_dict: dict = vars(spotify_track)

        for key in gpm_dict:
            gpm_value: str = str(gpm_dict.get(key)).lower()
            spotify_value: str = str(spotify_dict.get(key)).lower()

            if gpm_value is not None and spotify_value is not None:
                common_attributes += 1
                score += fuzz.partial_ratio(gpm_value, spotify_value)

        return int(score / common_attributes)

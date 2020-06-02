from exceptions.spotify.search_exceptions import NoMatchException
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

        """

        # Convert GPM Track To Search String
        search_string: str = SearchWrapper.__get_search_query(gpm_track=GpmTrack)

        # Search Spotify API using all available criteria

        # Search Spotify using relaxed criteria if no results returned

        # Raise NoMatchException if we still don't have any results

        # Score our results

        # Pick the result with the highest score

        # Convert it to a Spotify Track

        # Return the track

        return None

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

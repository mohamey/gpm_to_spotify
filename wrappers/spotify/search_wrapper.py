from exceptions.spotify.search_exceptions import NoMatchException
from meta.structures.track import GpmTrack, SpotifyTrack
from spotipy import Spotify

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

        # Search Spotify API using all available criteria

        # Search Spotify using relaxed criteria if no results returned

        # Raise NoMatchException if we still don't have any results

        # Score our results

        # Pick the result with the highest score

        # Convert it to a Spotify Track

        # Return the track

        return None

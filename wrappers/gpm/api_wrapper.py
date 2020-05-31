from exceptions.gpm.api_exceptions import UnauthenticatedClientException
from gmusicapi import Mobileclient
from meta.structures.track import GpmTrack
from typing import List


class ApiWrapper:
    """
    This Wrapper is responsible for handling the API calls for interacting with a users Google Play Music Account. This
    class doesn't handle Authentication, refer to the ``AuthWrapper`` for authentication.
    """

    @staticmethod
    def get_library(mobile_client: Mobileclient) -> List[GpmTrack]:
        """
        Given an authenticated mobile client, return a list of GPM Tracks representing the users library

        Args:
            mobile_client (Mobileclient): Must be authenticated. Client is used to retrieve the library for the GPM
                user.

        Returns:
            List[GpmTrack]: A list of ``GpmTrack`` objects representing the user's library.

        """
        # Check if client isn't authenticated
        if not mobile_client.is_authenticated():
            raise UnauthenticatedClientException("Trying to get library with an unauthenticated mobile client")

        # Get the library as a list of dicts
        raw_tracks: List[dict] = mobile_client.get_all_songs()

        return [ApiWrapper.__map_dict_to_gpm_track(track) for track in raw_tracks]

    @staticmethod
    def __map_dict_to_gpm_track(track_dict: dict) -> GpmTrack:
        """
        This maps a JSON Object returned by the Skyjam API representing a track into a GpmTrack Object. No checking for
        Nones.

        Args:
            track_dict (dict): A dict mapping of a JSON Object from the Skyjam API representing a track

        Returns:
            GpmTrack: A GpmTrack representing the track returned by Skyjam

        Todo:
            * Get Genre from the dict return by Skyjam and map it to the GpmTrack

        """

        return GpmTrack(
            title=track_dict.get('title'),
            artist=track_dict.get('artist'),
            album=track_dict.get('album'),
            year=track_dict.get('year')
        )


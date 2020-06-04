from spotipy import Spotify
from typing import List


class LibraryWrapper:

    @staticmethod
    def update_user_library(spotify: Spotify, uris: List[str]) -> int:
        """
        This method takes an authenticated spotify object for a user with the correct scope required to update the users
        saved tracks, and a list of tracks to update the users shared library with

        Args:
            spotify (Spotify): An authenticated spotify object to update a user's library with
            uris (List[str]): A list of URIs to update the user's library with

        Returns:
            int: Representing the number of tracks we failed to update

        Todo:
            * Add better error handling logic
            * Add proper logging

        """

        if len(uris) == 0:
            print("No Uris provided")
            return 0

        failed_update_count: int = 0
        for uri_subset in LibraryWrapper.__uri_subset_generator(uris):
            try:
                spotify.current_user_saved_tracks_add(uri_subset)
            except: # Catch any error for now, loop back to error handling
                failed_update_count += len(uri_subset)

        return failed_update_count

    @staticmethod
    def __uri_subset_generator(uris: List[str], list_size: int = 50) -> List[str]:
        """
        Generator that will split a long list into smaller subsets that can be used with the spotify API

        Args:
            uris (List[str]): List of URIs that needs to be split into sub-lists
            list_size (int): Maximum size of each list subset

        Returns:
            List[str]: A list of maximum size ``list_size`` that can be used with the Python API

        """

        current_index: int = 0
        max_index: int = len(uris)

        while current_index < max_index:
            end_index = min(max_index, current_index + list_size)
            yield uris[current_index:end_index]

            current_index = end_index
            print(f"Finished processing {current_index} of {max_index} tracks")

from spotipy import Spotify
from typing import List
from unittest import TestCase
from unittest.mock import MagicMock
from wrappers.spotify.library_wrapper import LibraryWrapper


class LibraryWrapperTest(TestCase):

    def test_update_library(self):
        mock_spotify_client: Spotify = MagicMock(Spotify)
        mock_uris: List[str] = [
            'spotify:track:1wGoqD0vrf7nj_dummy_uri_1',
            'spotify:track:1wGoqD0vrf7nj_dummy_uri_2'
        ]

        failed_updates: int = LibraryWrapper.update_user_library(spotify=mock_spotify_client, uris=mock_uris)

        self.assertEqual(0, failed_updates)
        mock_spotify_client.current_user_saved_tracks_add.assert_called_with(mock_uris)

    def test_update_library_with_failed_tracks(self):
        mock_spotify_client: Spotify = MagicMock(Spotify)
        mock_uris: List[str] = [
            'spotify:track:1wGoqD0vrf7nj_dummy_uri_1',
            'spotify:track:1wGoqD0vrf7nj_dummy_uri_2'
        ]

        mock_spotify_client.current_user_saved_tracks_add.side_effect = Exception("Mimicking network exception here")
        failed_updates = LibraryWrapper.update_user_library(spotify=mock_spotify_client, uris=mock_uris)

        mock_spotify_client.current_user_saved_tracks_add.assert_called_with(mock_uris)
        self.assertEqual(2, failed_updates)

    def test_update_library_with_no_tracks(self):
        mock_spotify_client: Spotify = MagicMock(Spotify)
        mock_uris: List[str] = []

        failed_updates = LibraryWrapper.update_user_library(spotify=mock_spotify_client, uris=mock_uris)

        mock_spotify_client.current_user_saved_tracks_add.assert_not_called()
        self.assertEqual(0, failed_updates)


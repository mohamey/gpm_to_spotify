from exceptions.spotify.search_exceptions import NoMatchException
from meta.structures.track import GpmTrack, SpotifyTrack
from spotipy import Spotify
from unittest.mock import MagicMock
from wrappers.spotify.search_wrapper import SearchWrapper

import unittest


class SearchWrapperTest(unittest.TestCase):
    """
    Testing the search wrapper, which is responsible for mapping GpmTracks to SpotifyTracks
    """

    def test_get_spotify_match(self):
        gpm_track: GpmTrack = GpmTrack(title='Test Title', artist='Test Artist')
        spotify_track: SpotifyTrack = SpotifyTrack(title='Test Title', artist='Test Artist', score=80, uri='Test Uri')

        mock_spotify_client: Spotify = MagicMock(Spotify)
        # TODO: Figure out the format of a Spotify result to be mapped correctly
        mock_spotify_client.search.return_result = {}

        # Get the spotify track from the search wrapper
        result: SpotifyTrack = SearchWrapper.get_spotify_match(spotify_client=mock_spotify_client, gpm_track=gpm_track)

        self.assertEqual(spotify_track, result)
        mock_spotify_client.search.assert_called_once()

    def test_get_spotify_match_with_no_match(self):
        gpm_track: GpmTrack = GpmTrack(title='Test Title', artist='Test Artist')

        mock_spotify_client: Spotify = MagicMock(Spotify)
        mock_spotify_client.search.return_result = []

        with self.assertRaises(NoMatchException) as context:
            # Get the spotify track from the search wrapper
            SearchWrapper.get_spotify_match(spotify_client=mock_spotify_client, gpm_track=gpm_track)

        self.assertEqual(NoMatchException, type(context.exception), "No match found for Gpm Track")
        mock_spotify_client.search.assert_called_once()

from exceptions.spotify.search_exceptions import NoMatchException
from json import load
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
        gpm_track: GpmTrack = GpmTrack(title='Any Colour You Like', artist='Pink Floyd',
                                       album='The Dark Side of the Moon')

        expected_spotify_track: SpotifyTrack = SpotifyTrack(title='Any Colour You Like - 2011 Remastered Version',
                                                            album='The Dark Side Of The Moon [Remastered] (Remastered Version)',
                                                            album_art_url='https://i.scdn.co/image/ab67616d0000485131c57b302f0e3aca46ab7561',
                                                            artist='Pink Floyd',
                                                            uri='spotify:track:1wGoqD0vrf7njGvxm8CEf5',
                                                            year='1973')

        mock_spotify_client: Spotify = MagicMock(Spotify)
        with open('test/resources/spotify/search_results.json', 'r') as search_results_file:
            mock_spotify_client.search.return_value = load(search_results_file)

        # Get the spotify track from the search wrapper
        result: SpotifyTrack = SearchWrapper.get_spotify_match(spotify_client=mock_spotify_client, gpm_track=gpm_track)

        self.assertEqual(expected_spotify_track.get_title(), result.get_title())
        self.assertEqual(expected_spotify_track.get_artist(), result.get_artist())
        self.assertEqual(expected_spotify_track.get_album(), result.get_album())
        self.assertEqual(expected_spotify_track.get_uri(), result.get_uri())
        self.assertEqual(expected_spotify_track.get_year(), result.get_year())

        mock_spotify_client.search.assert_called_once()

    def test_get_spotify_match_with_no_match(self):
        gpm_track: GpmTrack = GpmTrack(title='Test Title', artist='Test Artist')

        mock_spotify_client: Spotify = MagicMock(Spotify)
        with open('test/resources/spotify/empty_search_results.json', 'r') as search_results_file:
            mock_spotify_client.search.return_value = load(search_results_file)

        with self.assertRaises(NoMatchException) as context:
            # Get the spotify track from the search wrapper
            SearchWrapper.get_spotify_match(spotify_client=mock_spotify_client, gpm_track=gpm_track)

        self.assertEqual(NoMatchException, type(context.exception), "No match found for Gpm Track")
        self.assertEqual(2, mock_spotify_client.search.call_count)

from exceptions.gpm.api_exceptions import MalformedTrackException, UnauthenticatedClientException
from gmusicapi import Mobileclient
from meta.structures.track import GpmTrack
from typing import List
from unittest.mock import MagicMock
from wrappers.gpm.api_wrapper import ApiWrapper

import unittest


class ApiWrapperTest(unittest.TestCase):
    """
    Given a mobile client that is authenticated, the ApiWrapperTest should get all the tracks in the library in the form
    of a List of GpmTracks
    """

    def test_get_library(self):
        # Set up our mocked mobile client
        mock_mobile_client: Mobileclient = MagicMock(Mobileclient)
        mock_mobile_client.is_authenticated.return_value = True
        mock_mobile_client.get_all_songs.return_value = [
            {
                'title': 'Test Title',
                'artist': 'Test Artist',
                'album': 'Test Album',
                'year': 1234
            }
        ]

        tracks: List[GpmTrack] = ApiWrapper.get_library(mobile_client=mock_mobile_client)

        self.assertEqual(type(tracks), list)
        self.assertEqual(type(tracks[0]), GpmTrack)
        self.assertEqual(len(tracks), 1)

        mock_mobile_client.is_authenticated.assert_called_once()
        mock_mobile_client.get_all_songs.assert_called_once()

    def test_get_library_with_unauthenticated_client(self):
        # Set up our mocked mobile client
        mock_mobile_client: Mobileclient = MagicMock(Mobileclient)
        mock_mobile_client.is_authenticated.return_value = False

        with self.assertRaises(UnauthenticatedClientException) as context:
            ApiWrapper.get_library(mobile_client=mock_mobile_client)

        mock_mobile_client.is_authenticated.assert_called_once()
        self.assertEqual(UnauthenticatedClientException, type(context.exception), "Tried to get library with \
                                                                                  unauthenticated client")

    def test_malformed_track_parsing_exception(self):
        # Set up our mocked mobile client
        mock_mobile_client: Mobileclient = MagicMock(Mobileclient)
        mock_mobile_client.is_authenticated.return_value = True
        # Track is missing mandatory fields
        mock_mobile_client.get_all_songs.return_value = [
            {
                'album': 'Test Album',
                'year': 1234
            }
        ]

        with self.assertRaises(MalformedTrackException) as context:
            ApiWrapper.get_library(mobile_client=mock_mobile_client)

        mock_mobile_client.is_authenticated.assert_called_once()
        mock_mobile_client.get_all_songs.assert_called_once()
        self.assertEqual(MalformedTrackException, type(context.exception), "Tried to parse a malformed track into a \
                                                                           GpmTrack")

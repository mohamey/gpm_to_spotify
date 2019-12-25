import unittest
from exceptions import gpm_exceptions
from gmusicapi import Mobileclient
from meta.structures.track import Track
from unittest.mock import MagicMock
from unittest.mock import patch
from wrappers import gpm_wrapper

class GpmWrapperTestCase(unittest.TestCase):

    def setUp(self):
        self.wrapper = gpm_wrapper.Wrapper()
        self.test_fp = "Test File Path"
        self.device_id = Mobileclient.FROM_MAC_ADDRESS

    """Handle Auth Flow tests"""
    def test_auth_flow_when_oauth_login_complete(self):
        mock_mobile_client = Mobileclient()
        mock_mobile_client.oauth_login = MagicMock(return_value=False)
        with patch.object(self.wrapper, 'SpotifyWrapper__', return_value=True) as patched_oauth_method,\
            patch.object(self.wrapper, '_Wrapper__login', return_value=True) as patched_login_method:

            auth_result = self.wrapper.handle_auth_flow(self.test_fp, self.device_id)
            patched_oauth_method.assert_called_once_with(self.test_fp)
            patched_login_method.assert_called_once_with(self.test_fp, self.device_id)

            self.assertTrue(auth_result, msg="Successfully logged in")

    def test_auth_flow_when_oauth_token_fails(self):
        with patch.object(self.wrapper, '_Wrapper__get_oauth_token', return_value=False) as patched_oauth_method:

            with self.assertRaises(gpm_exceptions.UnableToGetOauthCredentials) as context:
                self.wrapper.handle_auth_flow(self.test_fp)

            self.assertEqual(gpm_exceptions.UnableToGetOauthCredentials, type(context.exception),
                             "Failed to retrieve oauth credentials, exception raised")
            patched_oauth_method.assert_called_once_with(self.test_fp)

    def test_auth_flow_when_login_fails(self):
        with patch.object(self.wrapper, '_Wrapper__get_oauth_token', return_value=True) as patched_oauth_method,\
            patch.object(self.wrapper, '_Wrapper__login', ) as patched_login_method:
            patched_login_method.side_effect = gpm_exceptions.UnableToLoginToService("Login Failed")

            with self.assertRaises(gpm_exceptions.UnableToLoginToService) as context:
                self.wrapper.handle_auth_flow(self.test_fp, self.device_id)

            self.assertEqual(gpm_exceptions.UnableToLoginToService, type(context.exception),
                             "Failed to login, exception raised")

            patched_oauth_method.assert_called_once_with(self.test_fp)
            patched_login_method.assert_called_once_with(self.test_fp, self.device_id)

    """Map library to Tracks Test"""
    def test_library_mapped_to_songs(self):
        songs_list = []
        # Append a song with all the attributes
        songs_list.append({
            'title': 'The Great Destroyer',
            'artist': 'Nine Inch Nails',
            'album': 'Year Zero',
            'year': '2007'
        })

        songs_list.append({
            'title': 'Lifeless Dead',
            'artist': 'Mad Season',
            'album': 'Above (Deluxe Edition}',
            'year': None
        })

        self.wrapper.set_library(songs_list)
        self.wrapper.map_song_library_to_tracks()

        tracks_list = self.wrapper.get_tracks()
        self.assertEqual(len(tracks_list), 2)

        for track in tracks_list:
            self.assertEqual(Track, type(track))

            for key in ['title', 'artist', 'album', 'year']:
                self.assertTrue(key in track)


if __name__ == "__main__":
    unittest.main()

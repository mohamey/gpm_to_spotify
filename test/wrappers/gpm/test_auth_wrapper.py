from exceptions.gpm.auth_exceptions import AuthException
from gmusicapi import Mobileclient
from wrappers.gpm.auth_wrapper import AuthWrapper
from unittest.mock import MagicMock

import unittest


class AuthWrapperTest(unittest.TestCase):

    def test_authenticate_mobile_client(self):
        dummy_code: str = 'valid_code'
        mocked_mobile_client: Mobileclient = MagicMock(Mobileclient)

        AuthWrapper.authenticate_mobile_client(mobile_client=mocked_mobile_client, code=dummy_code)

        mocked_mobile_client.perform_oauth.assert_called_once_with(storage_filepath=None, code=dummy_code)
        mocked_mobile_client.oauth_login.assert_called_once()

    def test_auth_failure_with_invalid_code(self):
        invalid_code: str = 'invalid_code'
        mocked_mobile_client: Mobileclient = MagicMock(Mobileclient)
        mocked_mobile_client.perform_oauth.side_effect = Exception('Perform Oauth Exception')

        with self.assertRaises(AuthException) as context:
            AuthWrapper.authenticate_mobile_client(mobile_client=mocked_mobile_client, code=invalid_code)

        self.assertEqual(AuthException, type(context.exception), "Failed to login, auth Exception raised")

    def test_auth_failure_with_invalid_oauth_cred(self):
        invalid_code: str = 'valid_code'
        mocked_mobile_client: Mobileclient = MagicMock(Mobileclient)
        mocked_mobile_client.oauth_login.side_effect = Exception('Oauth Login Exception')

        with self.assertRaises(AuthException) as context:
            AuthWrapper.authenticate_mobile_client(mobile_client=mocked_mobile_client, code=invalid_code)

        self.assertEqual(AuthException, type(context.exception), "Failed to login, auth Exception raised")

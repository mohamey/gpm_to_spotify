from exceptions.gpm.auth_exceptions import AuthException
from gmusicapi import Mobileclient
from oauth2client.client import OAuth2Credentials
from wrappers.gpm.auth_wrapper import AuthWrapper
from unittest.mock import MagicMock
from unittest import mock

import unittest


class AuthWrapperTest(unittest.TestCase):

    def test_authenticate_mobile_client(self):
        mocked_credentials: OAuth2Credentials = MagicMock(OAuth2Credentials)
        mocked_mobile_client: Mobileclient = MagicMock(Mobileclient)

        AuthWrapper.authenticate_mobile_client(mobile_client=mocked_mobile_client, oauth_credentials=mocked_credentials)

        mocked_mobile_client.perform_oauth.assert_not_called()
        mocked_mobile_client.oauth_login.assert_called_once_with(oauth_credentials=mocked_credentials,
                                                                 device_id=mock.ANY)

    def test_auth_failure_with_invalid_code(self):
        mocked_mobile_client: Mobileclient = MagicMock(Mobileclient)
        mocked_mobile_client.perform_oauth.side_effect = Exception('Perform Oauth Exception')

        with self.assertRaises(AuthException) as context:
            AuthWrapper.authenticate_mobile_client(mobile_client=mocked_mobile_client)

        self.assertEqual(AuthException, type(context.exception), "Failed to login, auth Exception raised")

    def test_auth_failure_with_invalid_oauth_cred(self):
        invalid_mocked_credentials: OAuth2Credentials = MagicMock(OAuth2Credentials)
        mocked_mobile_client: Mobileclient = MagicMock(Mobileclient)
        mocked_mobile_client.oauth_login.side_effect = Exception('Oauth Login Exception')

        with self.assertRaises(AuthException) as context:
            AuthWrapper.authenticate_mobile_client(mobile_client=mocked_mobile_client,
                                                   oauth_credentials=invalid_mocked_credentials)

        self.assertEqual(AuthException, type(context.exception), "Failed to login, auth Exception raised")

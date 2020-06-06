from exceptions.gpm.auth_exceptions import AuthException
from gmusicapi.clients.mobileclient import Mobileclient
from oauth2client.client import OAuth2Credentials


class AuthWrapper:
    """
    AuthWrapper is a GPM Wrapper class responsible for authenticating a mobile client for the gmusicapi
    """

    @staticmethod
    def authenticate_mobile_client(mobile_client: Mobileclient, code: str = None,
                                   device_id: str = Mobileclient.FROM_MAC_ADDRESS) -> Mobileclient:
        """
        This static method is responsible for taking a mobile client and authenticating it with the gmusicapi

        Args:
            mobile_client (Mobileclient): This is an unauthenticated mobile client to be authenticated with the
                Skyjam API through OAuth2
            code (str): The Auth Code provided from the user prompt, to be sent to the Auth Server to retrieve Oauth
                Credentials
            device_id (str): Device ID To be used by the Mobile Client. Defaults to the servers MAC Address.

        Returns:
            Mobileclient: Returns an authenticated mobile client

        Raises:
            AuthException: Raised when there was an issue performing the oauth token exchange with the auth server, or an issue
                authenticating the mobile client.

        TODO:
            * Add Oauth Token exchange for when a code is supplied by the client

        """

        try:
            # Authenticate mobile client, return it
            if code is None:
                oauth_credentials: OAuth2Credentials = mobile_client.perform_oauth(storage_filepath=None)
            else:
                oauth_credentials: OAuth2Credentials = mobile_client.perform_oauth(storage_filepath=None, code=code)

            mobile_client.oauth_login(oauth_credentials=oauth_credentials, device_id=device_id)

            return mobile_client

        except Exception as e:
            raise AuthException(e)


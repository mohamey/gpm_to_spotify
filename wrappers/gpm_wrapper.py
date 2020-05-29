from exceptions.gpm_exceptions import *
from meta.structures.track import GpmTrack
from os import path
from pymaybe import maybe
from typing import List, TypeVar

import sys

# Update Python Path to use patched gmusicapi
sys.path.append(path.abspath('../gmusicapi'))
from gmusicapi.clients.mobileclient import Mobileclient

# Define Types
T = TypeVar('T')


class GpmWrapper:
    """
    This is a wrapper that is responsible for interacting with the Skyjam API through the gmusicapi. This wrapper uses
    a modified version of the gmusicapi that is available here - https://github.com/mohamey/gmusicapi

    Attributes:
        mobile_client (Mobileclient): Spoofs a google play music mobile client
        tracks (List[GpmTrack]): A list of google play music tracks retrieved from the user's library

    Todo:
        * Refactor this class to be stateless.
    """

    def __init__(self, config: dict):
        self.__library: List[dict] = []
        self.__oauth_path: str = config[
            'oauth_path']  # TODO: This should not go to prod, cred shouldn't be stored on disk

        self.mobile_client: Mobileclient = Mobileclient()
        self.tracks: List[GpmTrack] = []

    def handle_auth_flow(self, device_id: str = Mobileclient.FROM_MAC_ADDRESS, code: str = None) -> bool:
        """
        This handles the auth flow for google play music. If no parameters are given, it'll work it's own params out.

        Args:
            device_id (str): Device ID to use for the mobile client. If none supplied, use the machines MAC Address
            code (str): The auth code to use. Will be passed from the Migrate UI

        Returns:
            bool: A boolean indicating whether or not auth was successful
        """

        if not self.__get_oauth_token(self.__oauth_path, code):
            raise UnableToGetOauthCredentials("Unable to get oauth credentials for GPM")

        self.__login(self.__oauth_path, device_id)

        # Got both the oauth token, and logged in. Return true to indicate success
        return True

    def get_song_library(self) -> None:
        """
        Assuming we're using an authenticated mobile client, get all the songs in the users library

        Returns:
            None: Nothing, we update the wrappers library attribute with the resulting List[dict]. This list of tracks
                from the skyjam API has more info than we actually care about
        """

        if self.mobile_client.is_authenticated():
            self.__library = self.mobile_client.get_all_songs()
        else:
            raise NotAuthenticatedException("Unable to perform authenticated requests at this time.")

    def map_song_library_to_tracks(self) -> None:
        """
        Take the songs we got from the skyjam API in the `get_song_libarary` method and transform them into a List of
        GPM Tracks we can use

        Returns:
            None: Nothing returned, update the wrapper's `tracks` attribute

        """

        for track in self.__library:
            try:
                self.tracks.append(GpmTrack(title=track['title'], artist=track['artist'],
                                            album=self.__get_optional_key(track, 'album'),
                                            year=self.__get_optional_key(track, 'year')))
            except KeyError as e:
                # TODO: Throw an actual exception here
                print(f"Failed to retrieve mandatory key {e} for track {maybe(track)['title']} - \
                    {maybe(track)['artist']}. Skipping.")

    @staticmethod
    def __get_optional_key(song: dict, key: str) -> T:
        """
        Given a dict from the GPM Library & a key, retrieve the value of the key from the dict. Return none if the
        key has no value

        Args:
            song (dict): A dict from the skyjam API
            key (str): A potential key in the dict

        Returns:
             T | None : A generic primitive represented by T, or None
        """

        try:
            return song[key]
        except KeyError:
            return None

    def get_tracks(self) -> List[GpmTrack]:
        """
        Return the list of GPM Tracks available in this wrapper

        Returns:
            List[GpmTrack]: The list of GPM Tracks stored in the tracks attribute of this wrapper
        """

        return self.tracks

    def set_library(self, library: List[dict]) -> None:
        """
        Given a raw list of songs retrieved from the Skyjam API for a users library, update the Wrappers library attribute

        Args:
            library (List[dict]): A list of songs retrieved from the Skyjam API

        Returns:
            None: Set the library attribute internally
        """

        self.__library = library

    def __get_oauth_token(self, oauth_file_path: str, code: str = None) -> bool:
        """
        Get an auth code, get the actual oauth token for a user. Can use a cached oauth token on the file system, or retrieve
        a new one using the supplied oauth code.

        Args:
            oauth_file_path (str): Cached credentials already on the disk. Should be deprecated soon since we don't want
             to be using cached tokens
            code (str): Oauth Code to be used to get the actual Oauth Token to authenticate with

        Returns:
            bool: Boolean indicating whether oauth token was retrieved

        Todo:
            * Get rid of token caching, leave that up to the client
        """

        if path.exists(oauth_file_path):
            with open(oauth_file_path) as oauth_file:
                oauth_cred = oauth_file.readlines()
        else:
            # No token found, get new one
            oauth_cred = self.mobile_client.perform_oauth(oauth_file_path, code=code)

        return oauth_cred is not None

    def __login(self, oauth_file_path: str, device_id: str = Mobileclient.FROM_MAC_ADDRESS) -> bool:
        """
        Authenticate the mobile client using credentials already on the disk.

        Args:
            oauth_file_path (str): Path to existing oauth credentials
            device_id (str): Device ID to be used for the mobile client. Defaults to the machines MAC Address

        Returns:
            bool: Boolean indicating whether login was successful or not

        Todo:
            * Deprecate this method, we don't want to be using credentials already on the disk.
        """

        if self.mobile_client.oauth_login(device_id, oauth_file_path):
            return True
        else:
            raise UnableToLoginToService(f"Login with device id {device_id}, oauth file path {oauth_file_path} failed")

from exceptions.gpm_exceptions import *
from meta.structures.track import Track
from os import path
from pymaybe import maybe

import sys

# Update Python Path to use patched gmusicapi
sys.path.append(path.abspath('../gmusicapi'))

from gmusicapi.clients.mobileclient import Mobileclient

class Wrapper:
    def __init__(self, config):
        self.__library = []
        self.__oauth_path = config['oauth_path'] # TODO: This should not go to prod, cred shouldn't be stored on disk

        self.mobile_client = Mobileclient()
        self.tracks = []

    def handle_auth_flow(self, device_id=Mobileclient.FROM_MAC_ADDRESS, code=None):
        if not self.__get_oauth_token(self.__oauth_path, code):
            raise UnableToGetOauthCredentials("Unable to get oauth credentials for GPM")

        self.__login(self.__oauth_path, device_id)

        # Got both the oauth token, and logged in. Return true to indicate success
        return True

    def get_song_library(self):
        if self.mobile_client.is_authenticated():
            self.__library = self.mobile_client.get_all_songs()
        else:
            raise NotAuthenticatedException("Unable to perform authenticated requests at this time.")

    def map_song_library_to_tracks(self):
        for track in self.__library:
            try:
                self.tracks.append(Track(title=track['title'], artist=track['artist'],
                                         album=self.__get_optional_key(track, 'album'),  # By default, if key doesn't exist None is returned
                                         year=self.__get_optional_key(track, 'year')))
            except KeyError as e:
                print(f"Failed to retrieve mandatory key {e} for track {maybe(track)['title']} - {maybe(track)['artist']}. Skipping.")

    def __get_optional_key(self, song, key):
        try:
            return song[key]
        except KeyError:
            return None

    def get_tracks(self):
        return self.tracks

    def set_library(self, library):
        self.__library = library

    def __get_oauth_token(self, oauth_file_path, code=None):
        # If token already exists on system, read it and check its not empty
        if path.exists(oauth_file_path):
            with open(oauth_file_path) as oauth_file:
                oauth_cred = oauth_file.readlines()
        else:
            # No token found, get new one
            oauth_cred = self.mobile_client.perform_oauth(oauth_file_path, code=code)

        return oauth_cred is not None

    def __login(self, oauth_file_path, device_id=Mobileclient.FROM_MAC_ADDRESS):
        # Assuming token is already available on file system, log in
        if self.mobile_client.oauth_login(device_id, oauth_file_path):
            return True
        else:
            raise UnableToLoginToService(f"Login with device id {device_id}, oauth file path {oauth_file_path} failed")

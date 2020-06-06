from exceptions.gpm.auth_exceptions import AuthException
from exceptions.spotify.search_exceptions import NoMatchException
from gmusicapi import Mobileclient
from json import load
from meta.structures.track import GpmTrack, SpotifyTrack
from spotipy import Spotify
from typing import List, Tuple
from wrappers.gpm.api_wrapper import ApiWrapper
from wrappers.gpm.auth_wrapper import AuthWrapper
from wrappers.spotify.library_wrapper import LibraryWrapper
from wrappers.spotify.search_wrapper import SearchWrapper
from sys import argv

import spotipy.util as util


class CLI:

    @staticmethod
    def run_cli(username: str):
        """
        This CLI Interface should just use basic prompts to get required tokens and migrate tracks to Spotify

        Returns:
            None

        Todo:
            * Parse Spotify Application Config from somewhere

        """

        # Load Spotify Config
        with open("cli-config.json") as config_file:
            spotify_config: dict = load(config_file)['spotify']['client']

        try:
            mobile_client: Mobileclient = AuthWrapper.authenticate_mobile_client(mobile_client=Mobileclient())
        except AuthException as e:
            print(f"Error getting an Authenticated Client for GPM:\n {e}")
            return

        # Get tracks using API Wrapper
        print("Getting your Library... ")
        gpm_library: List[GpmTrack] = ApiWrapper.get_library(mobile_client=mobile_client)
        print(f"Done. Found {len(gpm_library)} tracks")

        # Get Spotify Matches using Search Wrapper
        auth_token: str = util.prompt_for_user_token(
            username=username,
            scope='user-library-read,user-library-modify',
            client_id=spotify_config['id'],
            client_secret=spotify_config['secret'],
            redirect_uri=spotify_config['redirect_uri']
        )

        spotify_client: Spotify = Spotify(auth=auth_token)

        matched_tracks: List[Tuple[GpmTrack, SpotifyTrack]] = []
        print("Matching your GPM Library To Spotify Tracks...")
        for progress, gpm_track in enumerate(gpm_library):
            if progress % 100 == 0 and progress != 0:
                print(f"Finished matching {progress} of {len(gpm_library)} tracks...")
            try:
                matched_tracks.append((gpm_track, SearchWrapper.get_spotify_match(spotify_client=spotify_client,
                                                                                  gpm_track=gpm_track)))
            except NoMatchException as e:
                print(f"{e} - Skipping.")

        print(f"Finished. Matched {len(matched_tracks)} of {len(gpm_library)} tracks")
        # Update user's library
        user_response: str = input(f"Would you like to upload {len(matched_tracks)} to Spotify? This action will not affect your GPM Library (y/n)\n> ")

        if user_response == 'y':
            print("Uploading...")
            LibraryWrapper.update_user_library(spotify=spotify_client, uris=[spotify_track.get_uri() for (_, spotify_track)
                                                                             in matched_tracks])
        elif user_response == 'n':
            print("Noted. Skipping Library Upload")
        else:
            print("Invalid response, try again")


if __name__ == '__main__':
    if not argv[1]:
        print("You must provide a username to be used with the CLI in the form python command_line_interface.py <username>")

    username: str = argv[1]
    CLI.run_cli(username=username)

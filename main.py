from exceptions.runtime_exceptions import InvalidConfigException
from json import load
from wrappers import gpm_wrapper, spotify_wrapper

if __name__ == '__main__':
    with open('config.json') as config_file:
        config = load(config_file)

    if not config:
        raise InvalidConfigException("Config is empty")

    gpm_wrapper = gpm_wrapper.GpmWrapper(config['gpm'])

    # Perform oauth (if necessary), then login to the service
    gpm_wrapper.handle_auth_flow()
    gpm_wrapper.get_song_library()
    gpm_wrapper.map_song_library_to_tracks()
    track_list = gpm_wrapper.get_tracks()

    spotify_wrapper = spotify_wrapper.SpotifyWrapper(config['spotify'])
    spotify_wrapper.handle_auth()
    spotify_wrapper.find_tracks(track_list)
    # spotify_wrapper.add_saved_tracks()

    print(f"Matched {len(spotify_wrapper.mapped_tracks)} of {len(track_list)} from Google Play Music.")

    print("Finished!")

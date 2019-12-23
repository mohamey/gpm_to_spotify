from wrappers import gpm_wrapper, spotify_wrapper

if __name__ == '__main__':
    # oauth_path = "./runtime/outh.cred"

    # gpm_wrapper = gpm_wrapper.Wrapper()

    # # Perform oauth (if necessary), then login to the service
    # gpm_wrapper.handle_auth_flow(oauth_path)
    # songs_library = gpm_wrapper.get_song_library()

    # print("Finished")

    spotify_wrapper = spotify_wrapper.SpotifyWrapper()
    spotify_wrapper.handle_auth()
    spotify_wrapper.get_user_saved_tracks()
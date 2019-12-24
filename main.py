from wrappers import gpm_wrapper, spotify_wrapper

if __name__ == '__main__':
    oauth_path = "Cred Path Here."

    gpm_wrapper = gpm_wrapper.Wrapper()

    # Perform oauth (if necessary), then login to the service
    gpm_wrapper.handle_auth_flow(oauth_path)
    gpm_wrapper.get_song_library()
    gpm_wrapper.map_song_library_to_tracks()
    track_list = gpm_wrapper.get_tracks()[:100]

    spotify_wrapper = spotify_wrapper.SpotifyWrapper()
    spotify_wrapper.handle_auth()
    for track in track_list:
        spotify_wrapper.find_track(track)

    print("Finished!")

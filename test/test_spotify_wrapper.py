from json import load
from meta.structures.track import Track
import unittest

from wrappers import spotify_wrapper

"""This class is going to be mostly Integration Tests, since there isn't much code without side effects here.
The whole wrapper centers around communicating with Spotify. We'll just have to hope Spotipy is well tested."""


class SpotifyWrapperTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(SpotifyWrapperTestCase, cls).setUpClass()
        with open('/home/yasir/Documents/Projects/gpm_to_spotify/.config.json') as config_file:
            cls.config = load(config_file)

        cls.wrapper = spotify_wrapper.SpotifyWrapper(SpotifyWrapperTestCase.config['spotify'])
        cls.wrapper.handle_auth()


    def setUp(self) -> None:
        self.track = Track(title="Ten Crack Commandments (2014 Remaster)", artist="The Notorious B.I.G.",
                      album="Life After Death (2014 Remastered Edition)", year="1997")


    """ Test functionality of track searching """

    def test_track_search_with_fully_populated_track(self):
        SpotifyWrapperTestCase.wrapper.find_tracks([self.track])

        mapped_tracks = self.wrapper.mapped_tracks
        self.assertTrue(len(mapped_tracks) == 1)
        for key in ['title', 'artist', 'album', 'uri']:
            self.assertTrue(key in mapped_tracks[0])

        SpotifyWrapperTestCase.wrapper.get_user_saved_tracks()

    def test_add_track_to_saved_tracks(self):
        track_with_uri = self.track.copy()
        track_with_uri['uri'] = 'spotify:track:1Z7C8ClE8UEaH70jCCeJH2'
        SpotifyWrapperTestCase.wrapper.add_saved_tracks([track_with_uri])

        # Check track is now in saved tracks
        matched_track = False
        for item in SpotifyWrapperTestCase.wrapper.get_user_saved_tracks()['items']:
            track = item['track']
            if track['uri'] == track_with_uri['uri']:
                matched_track = True
                break

        self.assertTrue(matched_track)




if __name__ == '__main__':
    unittest.main()

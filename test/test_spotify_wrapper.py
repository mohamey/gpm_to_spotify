from meta.structures.track import Track
import unittest

from wrappers import spotify_wrapper


class SpotifyWrapperTestCase(unittest.TestCase):

    """ Test functionality of track searching """
    def test_track_search_with_fully_populated_track(self):
        track = Track(title="Ten Crack Commandments (2014 Remaster)", artist="The Notorious B.I.G.",
                      album="Life After Death (2014 Remastered Edition)", year="1997")

        wrapper = spotify_wrapper.SpotifyWrapper()
        wrapper.handle_auth()
        wrapper.find_track(track)


if __name__ == '__main__':
    unittest.main()

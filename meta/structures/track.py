from exceptions.gpm.api_exceptions import GpmMalformedTrackException
from exceptions.spotify.search_exceptions import SpotifyMalformedTrackException
from json import JSONEncoder
from re import sub


class GpmTrack:
    """
    A class used to define a google play music track. Doing this because just passing around dictionaries is too painful

    Attributes:
        title (str): Mandatory. The title of the track
        artist (str): Mandatory. The name of the artist
        album (str): The name of the album the track belongs to
        year (str): The year the track was released
        genre (str): The genre of the track

    Raises:
        GpmMalformedTrackException: When trying to create a GpmTrack without at least one of the mandatory attributes.
    """

    def __init__(self, title: str, artist: str, album: str = None, year: str = None, genre: str = None):
        if title is None or artist is None:
            raise GpmMalformedTrackException("Title and Artist cannot be None.")

        self.title: str = GpmTrack.__normalise(title)
        self.artist: str = GpmTrack.__normalise(artist)
        self.album: str = album
        self.year: str = year
        self.genre: str = genre

    def get_title(self) -> str:
        return self.title

    def get_artist(self) -> str:
        return self.artist

    def get_album(self) -> str:
        return self.album

    def get_year(self) -> str:
        return self.year

    def get_genre(self) -> str:
        return self.genre

    @staticmethod
    def __normalise(input: str) -> str:
        """
        Strip brackets and it's contents, then strip non-alphanumeric characters
        Args:
            input:

        Returns:

        """
        return sub(" ?[\(\[][^)]+[\)\]]", "", str(input)).replace('\'', '').replace(',', ' ')


class SpotifyTrack:
    """
    A class used to define a spotify track. Doing this because just passing around dictionaries is too painful.

    Attributes:
        title (str): Mandatory. The title of the track
        artist (str): Mandatory. The name of the artist
        uri (str): Mandatory. The spotify track's uri string
        album (str): The name of the album the track belongs to
        album_art_url (str): Link to the album art
        score (int): Score of the match for this Spotify Track with the original GPM Track
        year (str): The year the track was released
        genre (str): The genre of the track

    Raises:
        SpotifyMalformedTrackException: When trying to create a Spotify Track without at least one of the mandatory
            attributes.
    """

    def __init__(self, title: str, artist: str, uri: str, album: str = None, album_art_url: str = None,
                 score: int = None, year: str = None, genre: str = None):
        if title is None or artist is None or uri is None:
            raise SpotifyMalformedTrackException("Title, Artist & URI Cannot be None")

        self.title: str = title
        self.artist: str = artist
        self.uri: str = uri
        self.album: str = album
        self.album_art_url: str = album_art_url
        self.score: int = score
        self.year: str = year
        self.genre: str = genre

    def set_score(self, score: int):
        self.score = score

    def get_score(self) -> int:
        return self.score

    def get_title(self) -> str:
        return self.title

    def get_artist(self) -> str:
        return self.artist

    def get_album(self) -> str:
        return self.album

    def get_year(self) -> str:
        return self.year

    def get_uri(self) -> str:
        return self.uri

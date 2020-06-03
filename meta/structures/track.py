from exceptions.gpm.api_exceptions import GpmMalformedTrackException
from exceptions.spotify.search_exceptions import SpotifyMalformedTrackException
from json import JSONEncoder


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

        self.title: str = title
        self.artist: str = artist
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


class MatchedTrack:
    """
    A class used to define the match up of a spotify track and a google play music track. It's essentially just a dict
    but we'll define a class to keep things Sane

    Attributes:
        gpm_track (GpmTrack): Mandatory. The gpmTrack object of the matching pair
        spotify_track (SpotifyTrack): Mandatory. The spotifyTrack object of the matching pair
    """
    def __init__(self, gpm_track: GpmTrack, spotify_track: SpotifyTrack):
        self.gpm_track: GpmTrack = gpm_track
        self.spotify_track: SpotifyTrack = spotify_track


class TrackEncoder(JSONEncoder):
    """
    Encodes Tracks as JSON.

    Todo:
        * Remove this.
    """
    def default(self, o):
        return o.__dict__

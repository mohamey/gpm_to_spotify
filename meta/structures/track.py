from json import JSONEncoder


class GpmTrack:
    """
    A class used to define a google play music track. Doing this because just passing around dictionaries is too painful

    Attributes:
        title (str): Mandatory. The title of the track
        artist (str): Mandatory. The name of the artist
        album (str): The name of the album the track belongs to
        year (int): The year the track was released
        genre (str): The genre of the track
    """

    def __init__(self, title: str, artist: str, album: str = None, year: int = None, genre: str = None):
        self.title: str = title
        self.artist: str = artist
        self.album: str = album
        self.year: int = year
        self.genre: str = genre


class SpotifyTrack:
    """
    A class used to define a spotify track. Doing this because just passing around dictionaries is too painful.

    Attributes:
        title (str): Mandatory. The title of the track
        artist (str): Mandatory. The name of the artist
        uri (str): Mandatory. The spotify track's uri string
        album (str): The name of the album the track belongs to
        year (int): The year the track was released
        genre (str): The genre of the track
    """

    def __init__(self, title: str, artist: str, uri: str, album: str = None, year: int = None, genre: str = None):
        self.title: str = title
        self.artist: str = artist
        self.uri: str = uri
        self.album: str = album
        self.year: int = year
        self.genre: str = genre


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

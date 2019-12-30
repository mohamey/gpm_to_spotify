""" This class is just a dict, but makes the code much easier to read in my opinion, since we're not just passing new
dictionaries around. This Dict has the following string fields:
* String title - Mandatory
* String artist - Mandatory
* String album - Optional
* String year - Optional
* String genre - Optional
* String spotify_uri - Mandatory for Songs mapped to Spotify after search
"""

class Track(dict):
    def __init__(self, *args, **kwargs):
        super(Track, self).__init__(*args, **kwargs)

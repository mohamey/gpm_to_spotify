from json import load, loads
from kafka import KafkaConsumer, KafkaProducer
from os import path
from wrappers.gpm_wrapper import Wrapper
from wrappers.spotify_wrapper import SpotifyWrapper

import logging
import sys

# Update Python Path to use patched gmusicapi
sys.path.append(path.abspath('../gmusicapi/gmusicapi'))

# Create the logger
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

# Load our config file
with open('config.json') as config_file:
    config = load(config_file)
    logger.info(f"Loaded the following config from file: {config}")



def get_kafka_consumer(config):
    logger.info(f"Creating a Kafka Consumer with the following config: {str(config)}")
    return KafkaConsumer(config['read-topics'],
                         bootstrap_servers=config['servers'],
                         auto_offset_reset=config['offset-reset'],
                         enable_auto_commit=True,
                         group_id=config['group'],
                         value_deserializer=lambda x: x.decode())


def get_kafka_producer(config):
    logger.info(f"Creating a Kafka Producer with the following config: {str(config)}")
    return KafkaProducer(bootstrap_servers=config['servers'],
                         value_serializer=lambda x: x.encode('utf-8'),
                         key_serializer=lambda x: x.encode('utf-8'))

def get_gpm_tracks(wrapper, auth_code):
    wrapper.handle_auth_flow(code=auth_code)
    wrapper.get_song_library()
    wrapper.map_song_library_to_tracks()
    return wrapper.get_tracks()

def get_mapped_tracks(spotify_wrapper, tracks):
    spotify_wrapper.handle_auth()
    spotify_wrapper.find_tracks(tracks)
    return spotify_wrapper.get_merged_tracks()

def get_gpm_library(message):
    """
    This method is responsible for logging into the users gpm account and retrieving all the songs in their library,
    then mapping each song to its Spotify counterpart. This takes some time, so might be worth while providing feedback.
    TODO:
        * Add Support for Playlists
        * Have input validation
        * Provide progress feedback
    :param message: Kafka message, should just contain a gpm oauth token.
    :return: Method does not return anything, but writes directly to the response Kafka Topic. Writes a list of MergedTrack
    objects to Kafka. Below is an example of a perfectly mapped MergedTrack Object that can be written:
    [
        {
            "gpm": {
                "title": "Blue Orchid",
                "artist": "The White Stripes",
                "album": "Get Behind Me Satan",
                "year": 2006
            },
            "spotify": {
                "title": "Blue Orchid",
                "artist": "The White Stripes",
                "album": "Get Behind Me Satan",
                "year": 2006,
                "uri": "spotify:track:0xNvZy7bfeMwksRfG8dYla"
            }
        }
    ]
    """

    gpm_wrapper = Wrapper(config['gpm'])
    spotify_wrapper = SpotifyWrapper(config['spotify'])
    code = str(message.value)
    try:
        # TODO: We're reading from the Kafka topic okay, but now we need to write the results back to another topic
        # TODO: We should also multithread this shit.
        # TODO: Patch gmusicapi to stop it from writing credentials to disk
        gpm_tracks = get_gpm_tracks(gpm_wrapper, code)
        merged_tracks = get_mapped_tracks(spotify_wrapper, gpm_tracks)

        # Throw it back on a topic
    except Exception as e:
        logger.error(f"There was an issue getting the library - {e}")
    finally:
        kafka_producer.send(topic=kafka_config['write-topics']['gpm_library'], value=merged_tracks, key=code)
        logger.info("Finished :)")


def update_spotify_account(message):
    """
    This method is responsible for updating user spotify libraries using messages read from a kafka topic that should
    contain the users oauth code and a list of track URIs to add to their spotify library.
    :param message: Message should be a kafka message, where the value is a JSON object that looks like:
    {
        "oauth-token": "ognsiusigunibgrir",
        "track-uris": ["list", "of", "uris"]
    }
    :return: Nothing returned by this method, though it should put some message on Kafka topic to frontend indicating
    success.
    """

    message_payload = loads(str(message.value))
    oauth_token = message_payload['oauth-token']
    track_uris = message_payload['track-uris']

    # Create our Spotify wrapper, authenticate with the users Token
    spotify_wrapper = SpotifyWrapper(config['spotify'])
    spotify_wrapper.handle_auth(token=oauth_token)

    # Update the users library
    spotify_wrapper.add_track_uris_to_library(track_uris)

    # Write something back to Kafka to provide feedback to the user


if __name__ == '__main__':
    kafka_config = config['kafka']

    kafka_consumer = get_kafka_consumer(kafka_config)
    logger.info("Kafka Consumer Created")

    kafka_producer = get_kafka_producer(kafka_config)
    logger.info("Kafka Producer Created")

    logger.info("Waiting for messages")
    for message in kafka_consumer:
        logger.info(f"Message received with value {message.value}")
        if message.topic == "gpm-auth":
            # We should be validating the message value isn't null, is a valid token
            get_gpm_library(message)
        elif message.topic == "spotify-migration":
            """
            We should be validating this is a JSON Object with the following keys:
            * oauth_token: The user's oauth token so we can update their library on their behalf
            * Spotify URIs: Just a list of URIs we're adding to their library
            """
            update_spotify_account(message)

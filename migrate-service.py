from json import load
from kafka import KafkaConsumer
from os import path
from wrappers.gpm_wrapper import Wrapper

import sys

# Update Python Path to use patched gmusicapi
sys.path.append(path.abspath('../gmusicapi/gmusicapi'))

if __name__ == '__main__':
    kafka_consumer = KafkaConsumer(
        'gpm_auth',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='gpm',
        value_deserializer=lambda x: x.decode()
    )

    with open('.config.json') as config_file:
        config = load(config_file)

    for message in kafka_consumer:
        try:
            # TODO: It's reading from the kafka topic okay, but we're getting an exception due to redirect uri mismatch
            wrapper = Wrapper(config['gpm'])
            wrapper.handle_auth_flow(code=str(message.value))
            wrapper.get_song_library()
            wrapper.map_song_library_to_tracks()
            print(len(wrapper.get_tracks()))
            print("Finished :)")
        except Exception as e:
            print(f"There was an issue getting the library - {e}")

        print(message.value)

from json import load, dumps
from kafka import KafkaConsumer, KafkaProducer
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

    kafka_producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                   value_serializer=lambda v: dumps(v).encode('utf-8'))

    with open('.config.json') as config_file:
        config = load(config_file)

    for message in kafka_consumer:
        wrapper = Wrapper(config['gpm'])
        code = str(message.value)
        try:
            # TODO: We're reading from the Kafka topic okay, but now we need to write the results back to another topic
            # TODO: We should also multithread this shit.
            # TODO: Patch gmusicapi to stop it from writing credentials to disk
            wrapper.handle_auth_flow(code=code)
            wrapper.get_song_library()
            wrapper.map_song_library_to_tracks()
            print(len(wrapper.get_tracks()))

            # Throw it back on a topic
        except Exception as e:
            print(f"There was an issue getting the library - {e}")
        finally:
            kafka_producer.send(topic="gpm_libraries", value=str(wrapper.get_tracks()), key=code.encode('utf-8'))
            print("Finished :)")


        print(message.value)

"""
Consumes raw trades from config.KAFKA_TOPIC_NAME_TRADES and produces OHLC data that is saved
to config.KAFKA_TOPIC_NAME_OHLC.
"""
import os
import logging

from quixstreams import Application

# import src.config as config
# from src.utils import initialize_logger, load_env_vars
# import config
from utils import initialize_logger, load_env_vars


logger = logging.getLogger()
load_env_vars()

# read environment variables
KAFKA_BROKER_ADDRESS = os.environ["KAFKA_BROKER_ADDRESS"]
KAFKA_INPUT_TOPIC = os.environ["KAFKA_INPUT_TOPIC"]
KAFKA_CONSUMER_GROUP = 'json__read_ohlc_consumer_group'
KAFKA_OUTPUT_TOPIC = os.environ["KAFKA_OUTPUT_TOPIC"]

def run():
    """
    Defines the processing task that ingests
    - raw trades from config.KAFKA_TOPIC_NAME_TRADES, and
    - produces OHLC data that is saved to config.KAFKA_TOPIC_NAME_OHLC.
    """
    # Define Quix your application and settings
    app = Application(
        broker_address=KAFKA_BROKER_ADDRESS,
        consumer_group=KAFKA_CONSUMER_GROUP,
        auto_offset_reset="earliest",
        consumer_extra_config={"allow.auto.create.topics": "true"},
        producer_extra_config={"allow.auto.create.topics": "true"},
    )

    # Define an input topic with JSON deserializer
    logger.info(f"Subscribing to topic {KAFKA_INPUT_TOPIC}")
    input_topic = app.topic(KAFKA_INPUT_TOPIC, value_deserializer="json")

    # Define an output topic with JSON serializer
    logger.info(f"Producing to topic {KAFKA_OUTPUT_TOPIC}")
    output_topic = app.topic(KAFKA_OUTPUT_TOPIC, value_serializer="json")

    # Create a StreamingDataFrame and start building your processing pipeline
    sdf = app.dataframe(input_topic)

    # Window the data into 1 minute intervals
    # TODO

    sdf = sdf.update(lambda val: print(f"Sending update: {val}"))

    # Send the message to the output topic
    sdf = sdf.to_topic(output_topic)

    # Start message processing
    app.run(sdf)


if __name__ == "__main__":
    initialize_logger(config_path="logging.yaml")

    run()
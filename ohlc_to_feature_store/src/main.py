import os
import logging

from quixstreams import Application

import config
from utils import initialize_logger, load_env_vars
from feature_store_api.api import FeatureStore

logger = logging.getLogger()
load_env_vars()

# read environment variables
KAFKA_BROKER_ADDRESS = os.environ["KAFKA_BROKER_ADDRESS"]
KAFKA_INPUT_TOPIC = os.environ["KAFKA_INPUT_TOPIC"]


def run():
    """
    Reads OHLC data from a Kafka topic and pushes the data to the Feature Store.
    """
    # Define Quix your application and settings
    app = Application(
        broker_address=KAFKA_BROKER_ADDRESS,
        consumer_group="json__save_ohlc_consumer_group",
        auto_offset_reset="earliest",
        consumer_extra_config={"allow.auto.create.topics": "true"},
        producer_extra_config={"allow.auto.create.topics": "true"},
    )

    # Define an input topic with JSON deserializer
    logger.info(f"Subscribing to topic {KAFKA_INPUT_TOPIC}")
    input_topic = app.topic(KAFKA_INPUT_TOPIC, value_deserializer="json")

    # Define some feature store access object
    feature_store = FeatureStore()

    # Create a feature group in the Feature Store
    feature_store.create_feature_group(config.OHLC_FEATURE_GROUP)

    # Create a StreamingDataFrame and push incoming messages to the FeatureStore using a custom function
    sdf = app.dataframe(topic=input_topic).update(
        lambda value: feature_store.write(value, config.OHLC_FEATURE_GROUP)
    )

    app.run(sdf)


if __name__ == "__main__":
    initialize_logger(config_path="logging.yaml")
    run()

"""
Consumes raw trades from config.KAFKA_TOPIC_NAME_TRADES and produces OHLC data that is saved
to config.KAFKA_TOPIC_NAME_OHLC.
"""
import os
import logging

from src.utils import initialize_logger, load_env_vars
# from utils import initialize_logger, load_env_vars


logger = logging.getLogger()
load_env_vars()

KAFKA_INPUT_TOPIC = os.environ["input"]
KAFKA_OUTPUT_TOPIC = os.environ["output"]
USE_LOCAL_KAFKA = True if os.environ.get('use_local_kafka') is not None else False


def run():
    """
    Defines the processing task that ingests
    - raw trades from config.KAFKA_TOPIC_NAME_TRADES, and
    - produces OHLC data that is saved to config.KAFKA_TOPIC_NAME_OHLC.
    """
    from src.app_factory import get_app
    app = get_app(use_local_kafka=USE_LOCAL_KAFKA)
    serializer = "json" if USE_LOCAL_KAFKA else "quix_timeseries"
    deserializer = "json" if USE_LOCAL_KAFKA else "quix"

    # Define an input topic with JSON deserializer
    logger.info(f"Subscribing to topic {KAFKA_INPUT_TOPIC}")
    input_topic = app.topic(KAFKA_INPUT_TOPIC, value_deserializer=deserializer)

    # Define an output topic with JSON serializer
    logger.info(f"Producing to topic {KAFKA_OUTPUT_TOPIC}")
    output_topic = app.topic(KAFKA_OUTPUT_TOPIC, value_serializer=serializer)

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
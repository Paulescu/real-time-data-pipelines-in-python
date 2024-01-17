"""
Consumes raw trades from config.KAFKA_TOPIC_NAME_TRADES and produces OHLC data that is saved
to config.KAFKA_TOPIC_NAME_OHLC.
"""
import os
import logging

from src.utils import initialize_logger, load_env_vars
from src.app_factory import get_app


logger = logging.getLogger()
load_env_vars()

KAFKA_INPUT_TOPIC = os.environ["input"]
KAFKA_OUTPUT_TOPIC = os.environ["output"]
USE_LOCAL_KAFKA = True if os.environ.get('use_local_kafka') is not None else False


def get_timestamp(val: dict, *_):
    return val["timestamp"] * 1000

def reduce_price(state: dict, val: dict) -> dict:
    state["last"] = val['price']
    state["min"] = min(state["min"], val['price']) 
    state["max"] = max(state["max"], val['price']) 

    return state

def init_reduce_price(val: dict) -> dict:    
    return {
        "last" : val['price'],
        "first": val['price'],
        "max": val['price'],
        "min": val['price'],
        "product_id": val['product_id'],
    }


def run():
    """
    Defines the processing task that ingests
    - raw trades from config.KAFKA_TOPIC_NAME_TRADES, and
    - produces OHLC data that is saved to config.KAFKA_TOPIC_NAME_OHLC.
    """
    # Define Quix your application and settings
    app = get_app(use_local_kafka=USE_LOCAL_KAFKA)

    # Define an input topic with JSON deserializer
    logger.info(f"Subscribing to topic {KAFKA_INPUT_TOPIC}")
    input_topic = app.topic(KAFKA_INPUT_TOPIC, value_deserializer="json")

    # Define an output topic with JSON serializer
    logger.info(f"Producing to topic {KAFKA_OUTPUT_TOPIC}")
    output_topic = app.topic(KAFKA_OUTPUT_TOPIC, value_serializer="json")

    # Create a StreamingDataFrame and start building your processing pipeline
    sdf = app.dataframe(input_topic)

    # Window the data into 10 second intervals
    sdf = sdf.tumbling_window(10, 0).reduce(reduce_price, init_reduce_price).final()

    # extract open, high, low, close
    sdf["open"] = sdf.apply(lambda v: v['value']['first'])
    sdf["high"] = sdf.apply(lambda v: v['value']['max'])
    sdf["low"] = sdf.apply(lambda v: v['value']['min'])
    sdf["close"] = sdf.apply(lambda v: v['value']['last'])
    
    # extract the `product_id` and `timestamp` keys
    sdf["product_id"] = sdf.apply(lambda v: v['value']['product_id'])
    sdf['timestamp'] = sdf.apply(lambda v: int(v['start']))

    # keep only the columns we want
    sdf = sdf[['product_id', 'timestamp',
               'open', 'high', 'low', 'close',
               'start', 'end']]

    sdf = sdf.update(lambda val: print(f"Sending update: {val}"))

    # Send the message to the output topic
    sdf = sdf.to_topic(output_topic)

    # Start message processing
    app.run(sdf)

if __name__ == "__main__":

    initialize_logger(config_path="logging.yaml")

    run()
"""
Connect to the Alpaca News API and dumps news into a Kafka topic.
This version works for a Kafka cluster running locally.
"""
import os
import logging

from quixstreams.kafka import Producer

# from src.utils import (
#     initialize_logger,
#     load_env_vars,
# )
# from src.kraken_api.api import KrakenTradesAPI
# from src import config
from utils import (
    initialize_logger,
    load_env_vars,
)
from kraken_api.api import KrakenTradesAPI
from config import PRODUCT_IDS

logger = logging.getLogger()
load_env_vars()

# read environment variables
KAFKA_BROKER_ADDRESS = os.environ["KAFKA_BROKER_ADDRESS"]
KAFKA_OUTPUT_TOPIC = os.environ["KAFKA_OUTPUT_TOPIC"]

def run():
    # alpaca API client object
    kraken_api_client = KrakenTradesAPI(product_ids=PRODUCT_IDS, log_enabled=False)
    kraken_api_client.subscribe()

    with Producer(
        broker_address=KAFKA_BROKER_ADDRESS,
        extra_config={"allow.auto.create.topics": "true"},
    ) as producer:
        while True:
            # read trades from Kraken API
            trades = kraken_api_client.get_trades()
            if not trades:
                continue

            # logger.info(f"Received {len(trades)} trades: {trades}")

            # produce trades to Kafka
            for trade in trades:
                value = trade.to_str()

                producer.produce(
                    topic=KAFKA_OUTPUT_TOPIC,
                    # headers=[("uuid", str(uuid.uuid4()))],  # a dict is also allowed here
                    key=trade.product_id,
                    value=value,
                )
                logger.info(f"Produced {value=} to {KAFKA_OUTPUT_TOPIC}")

if __name__ == "__main__":
    initialize_logger(config_path="logging.yaml")

    run()

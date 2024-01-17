import os
import logging
from typing import Optional
import uuid

import fire

from src.utils import (
    initialize_logger,
    load_env_vars,
)
from src.kraken_api.api import KrakenTradesAPI
from src.producer_wrapper import ProducerWrapper


logger = logging.getLogger()
load_env_vars()

USE_LOCAL_KAFKA = True if os.environ.get('use_local_kafka') is not None else False
KAFKA_OUTPUT_TOPIC = os.environ["output"]

PRODUCT_IDS = ["XBT/EUR", "XBT/USD"]


def run():

    # Kraken API client
    kraken_api_client = KrakenTradesAPI(product_ids=PRODUCT_IDS,
                                        log_enabled=False)
    kraken_api_client.subscribe()

    with ProducerWrapper(KAFKA_OUTPUT_TOPIC, USE_LOCAL_KAFKA) as producer:
        
        while True:
            # read trades from Kraken API
            trades = kraken_api_client.get_trades()
            if not trades:
                continue

            logger.info(f"Received trades={trades} from Kraken API")

            # produce trades to Kafka
            for trade in trades:
                producer.produce(
                    # key=trade.product_id,
                    key=trade.product_id.replace("/", "-"),
                    # value=trade.to_str(),
                    value=trade.to_dict(),
                    headers=[("uuid", str(uuid.uuid4()))],  # a dict is also allowed here
                )

                logger.info(f"Produced {trade.to_str()=} with key={trade.product_id} to {KAFKA_OUTPUT_TOPIC}")

if __name__ == "__main__":

    initialize_logger(config_path="logging.yaml")
    fire.Fire(run)
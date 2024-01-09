"""
Connect to the Alpaca News API and dumps news into a Kafka topic
"""

import uuid
import logging

from quixstreams.kafka import Producer
from quixstreams.models.serializers import (
    QuixTimeseriesSerializer,
    SerializationContext,
)
from quixstreams.platforms.quix import QuixKafkaConfigsBuilder, TopicCreationConfigs

from src.utils import (
    initialize_logger,
    load_env_vars,
)
from src.kraken_trades_api import KrakenTradesAPI
import src.config as config

logger = logging.getLogger()
load_env_vars()


def run():
    # alpaca API client object
    kraken_api_client = KrakenTradesAPI(product_ids=config.PRODUCT_IDS)
    kraken_api_client.subscribe()

    # setup Kafka producer for Quix platform
    # For non-"Application.Quix" platform producing, config is a bit manual right now
    topic = config.KAFKA_TOPIC_NAME_TRADES  # "qts__purchase_events"
    cfg_builder = QuixKafkaConfigsBuilder()
    cfgs, topics, _ = cfg_builder.get_confluent_client_configs([topic])
    topic = topics[0]
    cfg_builder.create_topics([TopicCreationConfigs(name=topic)])
    serialize = QuixTimeseriesSerializer()

    with Producer(broker_address=cfgs.pop("bootstrap.servers"), extra_config=cfgs) as producer:
        while True:
            # read trades from Kraken API
            trades = kraken_api_client.get_trades()
            if not trades:
                continue

            logger.info(f"Received {len(trades)} trades: {trades}")

            # produce trades to Kafka topic
            for trade in trades:
                headers = {**serialize.extra_headers, "uuid": str(uuid.uuid4())}
                producer.produce(
                    topic=config.KAFKA_TOPIC_NAME_TRADES,
                    headers=headers,
                    key=trade.product_id,
                    value=trade.to_dict(),
                    ctx=SerializationContext(topic=topic, headers=headers),
                )
                logger.info("Produced value to Kafka.")


if __name__ == "__main__":
    initialize_logger(config_path="logging.yaml")

    run()

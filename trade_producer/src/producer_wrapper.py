from typing import Optional, Dict
import os
import json
import logging

from quixstreams.kafka import Producer
# from quixstreams.models.serializers import (
#     QuixTimeseriesSerializer,
#     SerializationContext,
# )
from quixstreams.platforms.quix import QuixKafkaConfigsBuilder, TopicCreationConfigs

logger = logging.getLogger()

class ProducerWrapper:
    """
    Wrapper around the quixstreams.kafka.Producer class, to handle both
    scenarios of
    - using local Kafka cluster or
    - Quix Kafka cluster.
    """
    def __init__(
        self,
        kafka_topic: str,
        use_local_kafka: Optional[bool] = False,
    ):
        # self._use_local_kafka = use_local_kafka
        self._kafka_topic = kafka_topic
        self._producer = None
        # self._serialize = None

        if use_local_kafka:
            
            logger.info("Connecting to Local Kafka cluster...")

            # Connect to local Kafka cluster.
            self._producer = Producer(
                broker_address=os.environ["KAFKA_BROKER_ADDRESS"],
                extra_config={"allow.auto.create.topics": "true"},
            )
        else:
            logger.info("Connecting to Quix Kafka cluster...")

            # Connect to Quix Kafka cluster.
            topic = kafka_topic
            cfg_builder = QuixKafkaConfigsBuilder()
            cfgs, topics, _ = cfg_builder.get_confluent_client_configs([topic])
            topic = topics[0]

            # Use the topic name returned by "cfg_builder". 
            # "cfg_builder" adds a prefix to the topic name that is required by the Quix platform
            self._kafka_topic = topic

            cfg_builder.create_topics([TopicCreationConfigs(name=topic)])

            # self._serialize = QuixTimeseriesSerializer()

            self._producer = Producer(
                broker_address=cfgs.pop("bootstrap.servers"),
                extra_config=cfgs
            )
            
    def produce(
        self,
        key,
        value: Dict[str, any],
        headers=None,
        partition=None,
        timestamp=None
    ):    
        self._producer.produce(
            topic=self._kafka_topic,
            headers=headers,
            key=key,
            value=json.dumps(value),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._producer.__exit__(exc_type, exc_value, traceback)

    
# from typing import Tuple
# def get_producer(
#     kafka_topic: str,
#     use_local_kafka: Optional[bool] = False,
# ) -> Producer:
#     """"""
#     if use_local_kafka:
#         logger.info(f"Connecting to Local Kafka cluster...")

#         # Connect to local Kafka cluster.
#         producer = Producer(
#             broker_address=os.environ["KAFKA_BROKER_ADDRESS"],
#             extra_config={"allow.auto.create.topics": "true"},
#         )
        
#     else:
#         logger.info(f"Connecting to Quix Kafka cluster...")

#         # Connect to Quix Kafka cluster.
#         topic = kafka_topic
#         cfg_builder = QuixKafkaConfigsBuilder()
#         cfgs, topics, _ = cfg_builder.get_confluent_client_configs([topic])
#         topic = topics[0]

#         # # Use the topic name returned by "cfg_builder". 
#         # # "cfg_builder" adds a prefix to the topic name that is required by the Quix platform
#         # kafka_topic = topic

#         cfg_builder.create_topics([TopicCreationConfigs(name=topic)])

#         # self._serialize = QuixTimeseriesSerializer()

#         producer = Producer(
#             broker_address=cfgs.pop("bootstrap.servers"),
#             extra_config=cfgs
#         )

#     return producer
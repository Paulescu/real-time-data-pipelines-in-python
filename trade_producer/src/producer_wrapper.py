from typing import Optional, Dict
import os
import json

from quixstreams.kafka import Producer
from quixstreams.models.serializers import (
    QuixTimeseriesSerializer,
    SerializationContext,
)
from quixstreams.platforms.quix import QuixKafkaConfigsBuilder, TopicCreationConfigs

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
        self._use_local_kafka = use_local_kafka
        self._kafka_topic = kafka_topic
        self._producer = None
        self._serialize = None

        if use_local_kafka:
            # Connect to local Kafka cluster.
            self._producer = Producer(
                broker_address=os.environ["KAFKA_BROKER_ADDRESS"],
                extra_config={"allow.auto.create.topics": "true"},
            )
        else:
            print("Connecting to Quix Kafka cluster...")
            
            # Connect to Quix Kafka cluster.
            topic = kafka_topic
            cfg_builder = QuixKafkaConfigsBuilder()
            cfgs, topics, _ = cfg_builder.get_confluent_client_configs([topic])
            topic = topics[0]
            cfg_builder.create_topics([TopicCreationConfigs(name=topic)])
            self._serialize = QuixTimeseriesSerializer()

            self._producer = Producer(
                broker_address=cfgs.pop("bootstrap.servers"),
                extra_config=cfgs
            )
            
    def produce(self, key, value: Dict[str, any], headers=None, partition=None, timestamp=None):

        # super().produce(topic, key, value, headers, partition, timestamp)
        if self._use_local_kafka:
            # Produce to local Kafka cluster.
            self._producer.produce(
                topic=self._kafka_topic,
                headers=headers,
                key=key,
                value=json.dumps(value),
            )
        else:
            # Produce to Quix Kafka cluster.
            self._producer.produce(
                topic=self._kafka_topic,
                headers=headers,
                key=key,
                value=self._serialize(
                    value=value,
                    ctx=SerializationContext(topic=self._kafka_topic, headers=headers)
                ),
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # super().__exit__(exc_type, exc_value, traceback)
        self._producer.__exit__(exc_type, exc_value, traceback)
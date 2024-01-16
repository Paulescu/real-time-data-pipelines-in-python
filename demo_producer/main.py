from typing import Optional, Dict
import os
import json
import logging
import uuid
import time
from random import randint, choice

from quixstreams.kafka import Producer
from quixstreams.models.serializers import (
    QuixTimeseriesSerializer,
    SerializationContext,
)
from quixstreams.platforms.quix import QuixKafkaConfigsBuilder, TopicCreationConfigs

topic = "new_topic_test"
cfg_builder = QuixKafkaConfigsBuilder()
cfgs, topics, _ = cfg_builder.get_confluent_client_configs([topic])
topic = topics[0]

# Use the topic name returned by "cfg_builder". 
# "cfg_builder" adds a prefix to the topic name that is required by the Quix platform
_kafka_topic = topic

cfg_builder.create_topics([TopicCreationConfigs(name=topic)])

serialize = QuixTimeseriesSerializer()

producer = Producer(
    broker_address=cfgs.pop("bootstrap.servers"),
    extra_config=cfgs
)


retailers = [
    "Billy Bob's Shop",
    "Tasty Pete's Burgers",
    "Mal-Wart",
    "Bikey Bikes",
    "Board Game Grove",
    "Food Emporium",
]

i = 0
with producer:
    while i < 10000:
        account = randint(0, 10)
        account_id = f"A{'0'*(10-len(str(account)))}{account}"
        value = {
            "account_id": account_id,
            "account_class": "Gold" if account >= 8 else "Silver",
            "transaction_amount": randint(-2500, -1),
            "transaction_source": choice(retailers),
        }
        print(f"Producing value {value}")
        producer.produce(
            topic=topic,
            headers=[("uuid", str(uuid.uuid4()))],  # a dict is also allowed here
            key=account_id,
            value=json.dumps(value),  # needs to be a string
        )
        i += 1
        if i % 5 == 0:
            time.sleep(5)
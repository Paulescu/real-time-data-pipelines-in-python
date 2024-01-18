import os
import logging
from typing import Optional

# import redis

from src.utils import initialize_logger, load_env_vars
from src.feature_store_api.api import FeatureStore
from src.feature_store_api.types import FeatureGroupConfig
from src.app_factory import get_app

logger = logging.getLogger()
load_env_vars()

KAFKA_INPUT_TOPIC = os.environ["input"]
USE_LOCAL_KAFKA = True if os.environ.get('use_local_kafka') is not None else False
OHLC_FEATURE_GROUP = FeatureGroupConfig(
    name='ohlc_feature_group',
    version=2,
    description='OHLC data for crypto products',
    primary_key=['timestamp', 'product_id'],
    event_time='timestamp',
    online_enabled=True,
)

def run():
    """
    Reads OHLC data from a Kafka topic and pushes the data to the Feature Store.
    """
    # Define Quix your application and settings
    app = get_app(
        consumer_group='ohlc-to-redis-consumer-group',
        use_local_kafka=USE_LOCAL_KAFKA,    
    )
    
    # Define an input topic with this deserializer
    input_topic = app.topic(KAFKA_INPUT_TOPIC, value_deserializer="json")

    # Define some feature store access object
    feature_store = FeatureStore()

    # Create a feature group in the Feature Store
    feature_group = feature_store.get_or_create_feature_group(OHLC_FEATURE_GROUP)

    # Create a StreamingDataFrame and push incoming messages to the FeatureStore using a custom function
    keys = ['timestamp', 'product_id', 'open', 'high', 'low', 'close']
    sdf = app.dataframe(topic=input_topic).update(
        lambda value: feature_group.write(value, keys=keys)
    )

    app.run(sdf)



if __name__ == "__main__":
    initialize_logger(config_path="logging.yaml")
    run()

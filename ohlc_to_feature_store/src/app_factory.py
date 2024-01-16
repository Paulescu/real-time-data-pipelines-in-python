import logging
import os
from typing import Optional

from quixstreams import Application

logger = logging.getLogger()

def get_app(
    consumer_group: str,
    use_local_kafka: Optional[bool] = False,
) -> Application:

    if use_local_kafka:
        logger.info(f"Creating Quix app for local environment")
        app = Application(
            broker_address=os.environ["KAFKA_BROKER_ADDRESS"],
            consumer_group=consumer_group,
            auto_offset_reset="earliest",
            consumer_extra_config={"allow.auto.create.topics": "true"},
            producer_extra_config={"allow.auto.create.topics": "true"},
        )
    
    else:
        logger.info(f"Creating Quix app for Quix Platform")
        app = Application.Quix(
            consumer_group=consumer_group,
            auto_offset_reset="earliest",
            auto_create_topics=True,  # Quix app has an option to auto create topics
        )
    
    return app
        



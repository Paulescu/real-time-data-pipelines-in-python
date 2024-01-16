import logging
import os
from typing import Optional
import time

import pandas as pd

from src.utils import initialize_logger, load_env_vars
from src.feature_store_api.api import FeatureStore
from src.feature_store_api.types import FeatureGroupConfig, FeatureViewConfig

initialize_logger()
load_env_vars()

logger = logging.getLogger()

OHLC_FEATURE_GROUP = FeatureGroupConfig(
    name='ohlc_feature_group',
    version=1,
    description='OHLC data for crypto products',
    primary_key=['timestamp', 'product_id'],
    event_time='timestamp',
    online_enabled=True,
)

OHLC_FEATURE_VIEW = FeatureViewConfig(
    name='ohlc_feature_view',
    version=1,
    description='OHLC feature view',
    feature_group_config=OHLC_FEATURE_GROUP,
)

def generate_list_primary_keys(
    from_unix_seconds: int,
    to_unix_seconds: int,
    product_ids: list,
) -> list:

    primary_keys = []

    for product_id in product_ids:
        for unix_seconds in range(from_unix_seconds, to_unix_seconds):
            primary_keys.append({
                'timestamp': unix_seconds,
                'product_id': product_id,
            })

    return primary_keys

def get_trades_last_5_minutes(
    last_minutes: int = 5,
    current_unix_seconds: Optional[int] = None,
    product_ids: Optional[list] = ['XBT/EUR'],
) -> pd.DataFrame:

    if current_unix_seconds is None:
        current_unix_seconds = int(time.time())

    logger.info("Connecting to Feature Store")
    feature_store = FeatureStore(
        api_key=os.environ["HOPSWORKS_API_KEY"],
        project_name=os.environ["HOPSWORKS_PROJECT_NAME"],
    )

    logger.info("Getting feature view to read data from")
    feature_view = feature_store.get_or_create_feature_view(OHLC_FEATURE_VIEW)

    from_unix_seconds = current_unix_seconds - last_minutes * 60
    logger.info(f"Getting data from {from_unix_seconds} to {current_unix_seconds}")
    primary_keys = generate_list_primary_keys(
        from_unix_seconds, 
        current_unix_seconds,
        product_ids)
    
    # breakpoint()

    trades : pd.DataFrame = feature_view.read(primary_keys)

    return trades

if __name__ == '__main__':

    trades = get_trades_last_5_minutes(last_minutes=1)
    print(trades)
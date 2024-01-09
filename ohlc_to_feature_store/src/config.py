# Feature Store parameters
from feature_store_api.types import FeatureGroupConfig

OHLC_FEATURE_GROUP = FeatureGroupConfig(
    name="ohlc_features",
    version=1,
    description="OHLC features for BTC/EUR and BTC/USD",
    primary_key=["product_id", "timestamp"],
    event_time="timestamp",
    online_enabled=True,
)

from typing import Optional, Union, List

from pydantic import BaseModel


class FeatureGroupConfig(BaseModel):
    """
    Represents a Feature Group in the Hopsworks Feature Store.

    Attributes:
        name (str): Name of the Feature Group
        version (int): Version of the Feature Group
        description (str): Description of the Feature Group
        primary_key (str): Primary key of the Feature Group
        online_enabled (bool): Whether the Feature Group is online enabled
        timestamp (datetime): Timestamp of the trade
    """

    name: str
    version: int
    description: Optional[str] = None
    primary_key: Union[str, List[str]]
    event_time: str
    online_enabled: Optional[bool] = True

    # def to_str(self) -> str:
    #     """
    #     Returns a string representation of the Trade object.
    #     """
    #     return json.dumps(self.model_dump())

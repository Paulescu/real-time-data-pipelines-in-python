import json
from typing import Dict

from pydantic import BaseModel


class Trade(BaseModel):
    """
    Represents a single trade.

    Attributes:
        price (float): Price of the trade
        volume (float): Volume of the trade
        timestamp (datetime): Timestamp of the trade
    """

    product_id: str
    price: float
    volume: float
    timestamp: int

    def to_str(self) -> str:
        """
        Returns a string representation of the Trade object.
        """
        return json.dumps(self.model_dump())

    def to_dict(self) -> Dict[str, any]:
        """
        Convert the Trade object to a dictionary.

        Returns:
            dict: A dictionary representation of the Trade object.
        """
        return {
            "product_id": self.product_id,
            "price": self.price,
            "volume": self.volume,
            "timestamp": self.timestamp,
            "Timestamp": self.timestamp, # required by Quix
        }
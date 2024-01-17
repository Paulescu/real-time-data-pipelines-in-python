from typing import List, Union, Optional, Dict, Any
import json
import logging

from websocket import create_connection

from .types import Trade

logger = logging.getLogger()


class KrakenTradesAPI:
    API_URL = "wss://ws.kraken.com"

    def __init__(
        self,
        product_ids: Optional[List[str]] = ["XBT/EUR"],
        log_enabled: bool = True,
    ):
        self._ws = None
        self.product_ids = product_ids
        self._log_enabled = log_enabled

    def subscribe(self):
        """
        Starts the websocket connection.
        """
        # open websocket connection
        self._ws = create_connection(self.API_URL)
        self._log(f"[KrakenTradesAPI]: Connected to {self.API_URL}")

        # subscribe to trades for the given `self.product_ids`
        self._ws.send(
            self._build_message(
                {
                    "event": "subscribe",
                    "pair": self.product_ids,
                    "subscription": {"name": "trade"},
                }
            )
        )

        # Receive systemStatus and subscriptionStatus events for each product_id
        # We do not need need to do anything with these messages, but we need to
        # receive them to keep the websocket connection alive.
        for _ in self.product_ids:
            # systemStatus event
            _ = self._recv()
            # subscriptionStatus event
            _ = self._recv()

    def _is_heartbeat(self, msg: Union[Dict, List[Any]]) -> bool:
        """
        Checks if a message is a heartbeat message.

        Args:
            msg (List[Dict]): The message to check.

        Returns:
            bool: True if the message is a heartbeat message, False otherwise.
        """
        if isinstance(msg, dict):
            return msg["event"] == "heartbeat"
        else:
            return False

    def get_trades(self) -> Union[None, List[Trade]]:
        """
        Fetches trades from the Alpaca News Stream and returns
        them as a list of Trade objects.
        """
        msg = self._recv()
        if self._is_heartbeat(msg):
            # skip heartbeat messages
            return None
        else:
            # parse list of dicts and return List[Trade]
            return self._parse_trades(msg)

    @staticmethod
    def _parse_trades(msg: List[Any]) -> List[Trade]:
        """
        Parses a message from the Alpaca News Stream into a list of Trade objects.
        """
        raw_trades = msg[1]
        trades = [
            Trade(
                product_id=msg[3],
                price=float(trade[0]),
                volume=float(trade[1]),
                # timestamp=datetime.utcfromtimestamp(int(float(trade[2])))
                timestamp=int(float(trade[2])) * 1000, # milliseconds
            )
            for trade in raw_trades
        ]
        return trades

    def _build_message(self, message: dict) -> str:
        """
        Builds a message to send to the Alpaca News Stream.

        Args:
            message (dict): The message to build.

        Returns:
            str: The built message.
        """
        return json.dumps(message)

    def _recv(self) -> Union[dict, List[dict]]:
        """
        Receives a message from the Alpaca News Stream.

        Returns:
            Union[dict, List[dict]]: The received message.
        """

        if self._ws:
            message = self._ws.recv()
            self._log(f"[KrakenTradeAPI]: Received message: {message}")
            message = json.loads(message)
            return message
        else:
            raise RuntimeError("Websocket not initialized. Call start() first.")

    def _log(self, msg: str) -> None:
        """
        Logs a message.

        Args:
            msg (str): The message to log.
        """
        if self._log_enabled:
            logger.info(msg)

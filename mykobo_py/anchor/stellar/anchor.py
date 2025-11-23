from typing import Optional
import requests
from time import time

from mykobo_py.anchor.stellar.models import Transaction


class AnchorRpcClient:
    def __init__(self, host, logger):
        self.host = host
        self.logger = logger

    def make_request(self, method, params):
        self.logger.info(f"Sending {method} request to {self.host}")
        payload = [
            {
                "jsonrpc": "2.0",
                "id": f"{int(time())}",
                "method": method,
                "params": params
            }
        ]
        self.logger.info(payload)
        url = f"{self.host}"
        try:
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            self.logger.error(f"Failed to make request to {self.host}: {e}")
            return None

    def get_transaction(self, transaction_id) -> Optional[Transaction]:
        try:
            response = requests.get(url=f"{self.host}/transactions/{transaction_id}")
            if response.ok:
                return Transaction.from_json(response.json())
            else:
                return None
        except Exception as e:
            self.logger.error(f"Failed to get transaction {transaction_id}: {e}")
            return None

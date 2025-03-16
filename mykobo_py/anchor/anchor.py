from typing import Optional
import requests
from time import time
from pprint import pprint

from mykobo_py.anchor.models import Transaction


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
        url = f"{self.host}"
        response = requests.post(url, json=payload)
        return response.json()

    def get_transaction(self, transaction_id) -> Optional[Transaction]:
        response = requests.get(url=f"{self.host}/transactions/{transaction_id}")
        if response.ok:
            return Transaction.from_json(response.json())
        else:
            return None

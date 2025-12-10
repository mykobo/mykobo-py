from typing import Optional
import requests
from time import time

from mykobo_py.anchor.stellar.models import Transaction


class AnchorRpcClient:
    def __init__(self, host, logger):
        self.host = host
        self.logger = logger

    def make_request(self, method, params):
        url = f"{self.host}"
        self.logger.info(f"Sending {method} request to {url}")
        payload = [
            {
                "jsonrpc": "2.0",
                "id": f"{int(time())}",
                "method": method,
                "params": params
            }
        ]
        self.logger.info(payload)

        try:
            response = requests.post(url, json=payload)
            print(f"Failed to make request to {self.host}: {response.content}")
            return response.json()
        except Exception as e:

            self.logger.error(f"Failed to make request to {self.host}: {e}")
            return None

    def get_transaction(self, transaction_id) -> Optional[Transaction]:
        self.logger.info(f"CLIENT: Fetching transaction {transaction_id}")
        if self.host.endswith("/"):
            url = self.host[:-1]
        else:
            url = self.host
        try:
            response = requests.get(url=f"{url}/transactions/{transaction_id}")
            if response.ok:
                return Transaction.from_json(response.json())
            else:
                self.logger.warning(f"CLIENT: Error fetching transaction {response.content}")
                return None
        except Exception as e:
            self.logger.error(f"CLIENT Failed to get transaction {transaction_id}: {e}")
            return e

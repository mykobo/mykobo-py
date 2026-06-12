from typing import Optional
import requests
from time import time

from mykobo_py.anchor.dapp.models import DappIntentPayload, Transaction
from mykobo_py.client import MykoboServiceClient
from mykobo_py.identity.models.auth import Token


class DappAnchorClient(MykoboServiceClient):
    def __init__(self, host, logger):
        super().__init__(logger, host)

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

    def get_transaction(self, service_token: Token, transaction_id, full_detail: bool = False) -> Optional[Transaction]:
        try:
            url = f"{self.host}/v1/transactions/{transaction_id}"
            self.logger.info(f"Getting transaction {transaction_id} from {url}")
            response = requests.get(
                url=url,
                params={"detail": "full"} if full_detail else None,
                headers=self.generate_headers(service_token, **{"Content-type": "application/json"}),
            )
            if response.ok:
                payload = response.json()
                return Transaction.model_validate(payload.get("transaction", payload))
            else:
                self.logger.error(f"Failed to get transaction {transaction_id}, response: {response.text}, {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to get transaction {transaction_id}: {e}")
            return None

    def create_transaction_intent(self, service_token: Token, payload: DappIntentPayload) -> Optional[Transaction]:
        try:
            url = f"{self.host}/v1/transactions/intent"
            self.logger.info(f"Creating transaction intent via {url}")
            response = requests.post(
                url=url,
                json=payload.model_dump(exclude_none=True),
                headers=self.generate_headers(service_token, **{"Content-type": "application/json"}),
            )
            if response.ok:
                data = response.json()
                return Transaction.model_validate(data.get("transaction", data))
            else:
                self.logger.error(
                    f"Failed to create transaction intent, response: {response.text}, {response.status_code}"
                )
                return None
        except Exception as e:
            self.logger.error(f"Failed to create transaction intent: {e}")
            return None

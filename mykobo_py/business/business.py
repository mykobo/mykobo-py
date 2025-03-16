from mykobo_py.client import MykoboServiceClient
import requests
from requests import Response
from typing import Optional

class BusinessServiceClient(MykoboServiceClient):
    def __init__(self, host, logger):
        super().__init__(logger, host)

    def get_fee(self, transaction_id: Optional[str], amount: Optional[str], kind: Optional[str], client_domain: Optional[str]) -> Response:
        url = f"{self.host}/fees"

        if transaction_id:
            url += f"?transaction_id={transaction_id}"
        if amount and not transaction_id:
            url += f"?value={amount}"
        if kind:
            url += f"&kind={kind}"
        if client_domain:
            url += f"&client_domain={client_domain}"

        response = requests.get(
            url
        )
        response.raise_for_status()
        return response

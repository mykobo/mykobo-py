from mykobo_py.business.models import FeeConfiguration
from mykobo_py.client import MykoboServiceClient
from mykobo_py.identity.models.auth import Token
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

    def new_fee(self, token: Token, configuration: FeeConfiguration) -> Response:
        url = f"{self.host}/new_fee"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            json=configuration.json()
        )
        response.raise_for_status()
        return response


    def all_fees(self, token: Token, configuration: FeeConfiguration) -> Response:
        url = f"{self.host}/fee_configurations"
        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"})
        )
        response.raise_for_status()
        return response
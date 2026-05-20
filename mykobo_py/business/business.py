import json

from mykobo_py.business.models import FeeConfiguration, TransactionLimitConfiguration
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
        url = f"{self.host}/fees/new"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            json=configuration.model_dump()
        )
        response.raise_for_status()
        return response


    def all_fees(self, token: Token) -> Response:
        url = f"{self.host}/fees/all"
        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"})
        )
        response.raise_for_status()
        return response

    def get_limit(
        self,
        transaction_type: str,
        asset: Optional[str] = None,
        user_id: Optional[str] = None,
        client_domain: Optional[str] = None,
    ) -> Response:
        url = f"{self.host}/limits?transaction_type={transaction_type}"

        if asset:
            url += f"&asset={asset}"
        if user_id:
            url += f"&user_id={user_id}"
        if client_domain:
            url += f"&client_domain={client_domain}"

        response = requests.get(url)
        response.raise_for_status()
        return response

    def new_limit(self, token: Token, configuration: TransactionLimitConfiguration) -> Response:
        url = f"{self.host}/limits/new"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            json=configuration.model_dump()
        )
        response.raise_for_status()
        return response

    def all_limits(self, token: Token, include_inactive: bool = False) -> Response:
        url = f"{self.host}/limits/all"
        if include_inactive:
            url += "?include_inactive=true"
        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"})
        )
        response.raise_for_status()
        return response
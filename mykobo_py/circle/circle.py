import json
from logging import Logger
from typing import Optional

import requests
from requests import Response

from mykobo_py.client import MykoboServiceClient
from mykobo_py.identity.models.auth import Token
from .models.request import CreateRelayAddressRequest


class CircleServiceClient(MykoboServiceClient):
    def __init__(self, host: str, logger: Logger):
        super().__init__(logger, host)

    def health(self) -> Response:
        response = requests.get(f"{self.host}/health")
        response.raise_for_status()
        return response

    def create_relay_address(self, token: Token, request: CreateRelayAddressRequest) -> Response:
        response = requests.post(
            f"{self.host}/relay-addresses",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(request.to_dict())
        )
        response.raise_for_status()
        return response

    def list_relay_addresses(self, token: Token, chain: Optional[str] = None) -> Response:
        url = f"{self.host}/relay-addresses"
        if chain:
            url += f"?chain={chain}"
        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def list_circle_addresses(
        self,
        token: Token,
        chain: Optional[str] = None,
        currency: Optional[str] = None,
        purpose: Optional[str] = None,
    ) -> Response:
        url = f"{self.host}/circle-addresses"
        params = {}
        if chain:
            params["chain"] = chain
        if currency:
            params["currency"] = currency
        if purpose:
            params["purpose"] = purpose

        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            params=params,
        )
        response.raise_for_status()
        return response

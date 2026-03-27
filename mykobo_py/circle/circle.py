import json
from logging import Logger
from typing import Optional

import requests
from requests import Response

from mykobo_py.client import MykoboServiceClient
from mykobo_py.identity.models.auth import Token
from .models.request import CreateRelayAddressPairRequest


class CircleServiceClient(MykoboServiceClient):
    def __init__(self, host: str, logger: Logger):
        super().__init__(logger, host)

    def health(self) -> Response:
        response = requests.get(f"{self.host}/health")
        response.raise_for_status()
        return response

    def create_relay_address_pair(self, token: Token, request: CreateRelayAddressPairRequest) -> Response:
        response = requests.post(
            f"{self.host}/relay-addresses/pair",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=request.model_dump_json(exclude_none=True)
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

    def list_transactions(
        self,
        token: Token,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        chain: Optional[str] = None,
        status: Optional[str] = None,
        asset: Optional[str] = None,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
    ) -> Response:
        url = f"{self.host}/transactions"
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if chain:
            params["chain"] = chain
        if status:
            params["status"] = status
        if asset:
            params["token"] = asset
        if sender:
            params["sender"] = sender
        if recipient:
            params["recipient"] = recipient

        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            params=params,
        )
        response.raise_for_status()
        return response

    def get_transaction(self, token: Token, transaction_id: str) -> Response:
        response = requests.get(
            f"{self.host}/transactions/{transaction_id}",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

from logging import Logger
from typing import Optional

import requests
from requests import Response

from mykobo_py.client import MykoboServiceClient

from .models.request import (
    CreateWatchedAddressRequest,
    UpdateWatchedAddressRequest,
)


class SensorServiceClient(MykoboServiceClient):
    """HTTP client for the sensor-api service.

    The sensor-api currently does not require authentication, so the token
    parameter on these methods is optional and only used to populate
    User-Agent / Authorization headers when supplied (for parity with the
    other MYKOBO service clients).
    """

    API_PREFIX = "/api/v1"

    def __init__(self, host: str, logger: Logger):
        super().__init__(logger, host)

    def health(self) -> Response:
        response = requests.get(f"{self.host}/health")
        response.raise_for_status()
        return response

    # --- Watched addresses ---

    def list_watched_addresses(
        self,
        token=None,
        chain: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> Response:
        params = {}
        if chain:
            params["chain"] = chain
        if enabled is not None:
            params["enabled"] = str(enabled).lower()

        response = requests.get(
            f"{self.host}{self.API_PREFIX}/watched-addresses",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            params=params,
        )
        response.raise_for_status()
        return response

    def get_watched_address(self, address_id: str, token=None) -> Response:
        response = requests.get(
            f"{self.host}{self.API_PREFIX}/watched-addresses/{address_id}",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def create_watched_address(
        self,
        request: CreateWatchedAddressRequest,
        token=None,
    ) -> Response:
        response = requests.post(
            f"{self.host}{self.API_PREFIX}/watched-addresses",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=request.model_dump_json(exclude_none=True),
        )
        response.raise_for_status()
        return response

    def update_watched_address(
        self,
        address_id: str,
        request: UpdateWatchedAddressRequest,
        token=None,
    ) -> Response:
        response = requests.patch(
            f"{self.host}{self.API_PREFIX}/watched-addresses/{address_id}",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=request.model_dump_json(exclude_none=True),
        )
        response.raise_for_status()
        return response

    def delete_watched_address(self, address_id: str, token=None) -> Response:
        response = requests.delete(
            f"{self.host}{self.API_PREFIX}/watched-addresses/{address_id}",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    # --- Chain transactions ---

    def list_chain_transactions(
        self,
        token=None,
        chain: Optional[str] = None,
        status: Optional[str] = None,
        recipient: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Response:
        params = {}
        if chain:
            params["chain"] = chain
        if status:
            params["status"] = status
        if recipient:
            params["recipient"] = recipient
        if limit is not None:
            params["limit"] = limit

        response = requests.get(
            f"{self.host}{self.API_PREFIX}/transactions",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            params=params,
        )
        response.raise_for_status()
        return response

    def get_chain_transaction(self, transaction_id: str, token=None) -> Response:
        response = requests.get(
            f"{self.host}{self.API_PREFIX}/transactions/{transaction_id}",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    # --- Intents ---

    def list_intents(
        self,
        token=None,
        chain: Optional[str] = None,
        matched: Optional[bool] = None,
        limit: Optional[int] = None,
    ) -> Response:
        params = {}
        if chain:
            params["chain"] = chain
        if matched is not None:
            params["matched"] = str(matched).lower()
        if limit is not None:
            params["limit"] = limit

        response = requests.get(
            f"{self.host}{self.API_PREFIX}/intents",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            params=params,
        )
        response.raise_for_status()
        return response

    def get_intent(self, intent_id: str, token=None) -> Response:
        response = requests.get(
            f"{self.host}{self.API_PREFIX}/intents/{intent_id}",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

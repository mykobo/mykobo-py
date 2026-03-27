import json

import requests
from requests import Response

from mykobo_py.client import MykoboServiceClient
from mykobo_py.identity.models.auth import Token
from mykobo_py.idenfy.models.requests import AccessTokenRequest, VerificationRequest


class IdenfyServiceClient(MykoboServiceClient):
    def __init__(self, host, logger):
        super().__init__(logger, host)

    def health(self) -> Response:
        """Check the health of the iDenfy gateway."""
        url = f"{self.host}/health"
        response = requests.get(url)
        response.raise_for_status()
        return response

    def create_verification(self, token: Token, request: VerificationRequest) -> Response:
        """
        Create a verification session with iDenfy.

        Optionally submits document images for Direct Processing when
        images are included in the request.

        Returns 200 on full success, 207 if token creation succeeded
        but document processing failed.
        """
        self.logger.info(f"Creating verification for {request.external_ref} at {self.host}...")
        url = f"{self.host}/verification"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(request.to_dict()),
        )
        response.raise_for_status()
        return response

    def get_access_token(self, token: Token, request: AccessTokenRequest) -> Response:
        """
        Legacy endpoint. Creates an iDenfy auth token directly.
        Prefer create_verification() for new integrations.
        """
        self.logger.info(f"Sending {request} to {self.host}...")
        url = f"{self.host}/access_token"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(request.to_dict()),
        )
        response.raise_for_status()
        return response

    def send_event(self, token: Token, payload: dict) -> Response:
        """
        Forward an iDenfy webhook event to the gateway.
        """
        self.logger.info(f"Sending iDenfy event to {self.host}...")
        url = f"{self.host}/event"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(payload),
        )
        response.raise_for_status()
        return response
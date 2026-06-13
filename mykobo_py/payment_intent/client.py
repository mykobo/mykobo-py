from logging import Logger

import requests

from mykobo_py.client import MykoboServiceClient
from mykobo_py.identity.models.auth import Token
from mykobo_py.payment_intent.models import CreateReferenceRequest


class PaymentIntentServiceClient(MykoboServiceClient):
    def __init__(self, host: str, logger: Logger):
        super().__init__(logger, host)

    def health_check(self) -> dict:
        response = requests.get(f"{self.host}/health")
        response.raise_for_status()
        return response.json()

    def create_reference(self, user_token: str, payload: CreateReferenceRequest) -> dict:
        token = Token.from_jwt(user_token)
        response = requests.post(
            f"{self.host}/payment-references",
            headers=self.generate_headers(
                token, **{"Content-type": "application/json"}
            ),
            json=payload.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return response.json()

    def get_reference_by_value(self, user_token: str, reference: str) -> dict:
        token = Token.from_jwt(user_token)
        response = requests.get(
            f"{self.host}/payment-references/{reference}",
            headers=self.generate_headers(
                token, **{"Content-type": "application/json"}
            ),
        )
        response.raise_for_status()
        return response.json()

    def get_references_by_user(self, user_token: str, profile_id: str) -> list:
        token = Token.from_jwt(user_token)
        response = requests.get(
            f"{self.host}/payment-references/user/{profile_id}",
            headers=self.generate_headers(
                token, **{"Content-type": "application/json"}
            ),
        )
        response.raise_for_status()
        return response.json()

    def delete_reference(self, user_token: str, reference: str) -> bool:
        token = Token.from_jwt(user_token)
        response = requests.delete(
            f"{self.host}/payment-references/{reference}",
            headers=self.generate_headers(
                token, **{"Content-type": "application/json"}
            ),
        )
        response.raise_for_status()
        return response.status_code == 204

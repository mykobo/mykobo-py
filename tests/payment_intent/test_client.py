import datetime
import logging

import jwt
import pytest
from requests.exceptions import HTTPError

from mykobo_py.payment_intent.client import PaymentIntentServiceClient
from mykobo_py.payment_intent.models import CreateReferenceRequest

logger = logging.getLogger("test")
host = "https://payment-intent.example.com"


def _make_token(sub: str = "urn:usrp:test-user") -> str:
    payload = {
        "sub": sub,
        "iat": int(datetime.datetime.now().timestamp()),
        "exp": int(
            (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()
        ),
        "aud": "mykobo",
        "scope": ["transaction:admin"],
    }
    return jwt.encode(payload, "secret", algorithm="HS256")


class TestPaymentIntentServiceClient:
    def test_client_initialization(self):
        client = PaymentIntentServiceClient(host, logger)
        assert client.host == host
        assert client.logger is logger

    def test_health_check(self, requests_mock):
        client = PaymentIntentServiceClient(host, logger)
        requests_mock.get(
            f"{host}/health",
            json={"status": "Ok", "message": "Payment Intent Service is running"},
        )

        response = client.health_check()

        assert response == {
            "status": "Ok",
            "message": "Payment Intent Service is running",
        }

    def test_create_reference(self, requests_mock):
        client = PaymentIntentServiceClient(host, logger)
        user_token = _make_token()
        payload = CreateReferenceRequest(
            profile_id="urn:usrp:test-user",
            wallet_address="GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
            client_domain="example.com",
        )

        requests_mock.post(
            f"{host}/payment-references",
            json={
                "id": "urn:dpref:a1b2c3d4e5f6",
                "profile_id": "urn:usrp:test-user",
                "reference": "MYK-P-ABC12345",
                "is_active": True,
                "wallet_address": "GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
                "client_domain": "example.com",
                "created_at": "2026-06-13 12:00:00",
            },
            status_code=201,
        )

        response = client.create_reference(user_token, payload)

        assert response["reference"] == "MYK-P-ABC12345"
        assert response["is_active"] is True
        assert (
            requests_mock.last_request.headers["Authorization"]
            == f"Bearer {user_token}"
        )
        assert requests_mock.last_request.headers["User-Agent"] == "urn:usrp:test-user"

    def test_get_reference_by_value(self, requests_mock):
        client = PaymentIntentServiceClient(host, logger)
        user_token = _make_token()

        requests_mock.get(
            f"{host}/payment-references/MYK-P-ABC12345",
            json={
                "id": "urn:dpref:a1b2c3d4e5f6",
                "profile_id": "urn:usrp:test-user",
                "reference": "MYK-P-ABC12345",
                "is_active": True,
                "wallet_address": "GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
                "created_at": "2026-06-13 12:00:00",
            },
        )

        response = client.get_reference_by_value(user_token, "MYK-P-ABC12345")

        assert response["reference"] == "MYK-P-ABC12345"
        assert (
            requests_mock.last_request.headers["Authorization"]
            == f"Bearer {user_token}"
        )

    def test_get_references_by_user(self, requests_mock):
        client = PaymentIntentServiceClient(host, logger)
        user_token = _make_token()

        requests_mock.get(
            f"{host}/payment-references/user/urn:usrp:test-user",
            json=[
                {
                    "id": "urn:dpref:a1b2c3d4e5f6",
                    "profile_id": "urn:usrp:test-user",
                    "reference": "MYK-P-ABC12345",
                    "is_active": True,
                    "wallet_address": "GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
                    "created_at": "2026-06-13 12:00:00",
                }
            ],
        )

        response = client.get_references_by_user(user_token, "urn:usrp:test-user")

        assert isinstance(response, list)
        assert len(response) == 1
        assert response[0]["reference"] == "MYK-P-ABC12345"
        assert (
            requests_mock.last_request.headers["Authorization"]
            == f"Bearer {user_token}"
        )
        assert requests_mock.last_request.headers["User-Agent"] == "urn:usrp:test-user"

    def test_delete_reference(self, requests_mock):
        client = PaymentIntentServiceClient(host, logger)
        user_token = _make_token()

        requests_mock.delete(
            f"{host}/payment-references/MYK-P-ABC12345",
            status_code=204,
        )

        result = client.delete_reference(user_token, "MYK-P-ABC12345")

        assert result is True
        assert (
            requests_mock.last_request.headers["Authorization"]
            == f"Bearer {user_token}"
        )

    def test_delete_reference_not_found(self, requests_mock):
        client = PaymentIntentServiceClient(host, logger)
        user_token = _make_token()

        requests_mock.delete(
            f"{host}/payment-references/MYK-P-MISSING",
            status_code=404,
        )

        with pytest.raises(HTTPError):
            client.delete_reference(user_token, "MYK-P-MISSING")

    def test_create_reference_conflict(self, requests_mock):
        client = PaymentIntentServiceClient(host, logger)
        user_token = _make_token()
        payload = CreateReferenceRequest(
            profile_id="urn:usrp:test-user",
            wallet_address="GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
        )

        requests_mock.post(
            f"{host}/payment-references",
            status_code=409,
            json={"message": "User already has an active reference for this wallet address"},
        )

        with pytest.raises(HTTPError):
            client.create_reference(user_token, payload)

    def test_get_reference_by_value_not_found(self, requests_mock):
        client = PaymentIntentServiceClient(host, logger)
        user_token = _make_token()

        requests_mock.get(
            f"{host}/payment-references/MYK-P-MISSING",
            status_code=404,
        )

        with pytest.raises(HTTPError):
            client.get_reference_by_value(user_token, "MYK-P-MISSING")

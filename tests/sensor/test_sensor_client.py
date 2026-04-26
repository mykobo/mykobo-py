import datetime
import json
import logging

import pytest
from requests.exceptions import HTTPError

from mykobo_py.identity.models.auth import Token
from mykobo_py.sensor.models.common import Chain, EnrichmentStrategy
from mykobo_py.sensor.models.request import (
    CreateWatchedAddressRequest,
    UpdateWatchedAddressRequest,
)
from mykobo_py.sensor.sensor import SensorServiceClient


logger = logging.getLogger("test")
host = "https://sensor.example.com"
test_token = Token(
    subject_id="urn:usrp:test",
    token="test_token",
    refresh_token="test_refresh",
    expires_at=datetime.datetime.now() + datetime.timedelta(days=30),
)


class TestSensorServiceClient:
    def test_client_initialization(self):
        client = SensorServiceClient(host, logger)
        assert client.host == host
        assert client.logger is logger
        assert client.API_PREFIX == "/api/v1"

    def test_health(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(f"{host}/health", json={"status": "ok"})

        response = client.health()

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_status(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(
            f"{host}/api/v1/status",
            json={"chains": {"STELLAR": "ok"}},
        )

        response = client.status()

        assert response.status_code == 200
        assert response.json() == {"chains": {"STELLAR": "ok"}}

    def test_list_watched_addresses_no_filters(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(
            f"{host}/api/v1/watched-addresses",
            json=[],
        )

        response = client.list_watched_addresses()

        assert response.status_code == 200
        assert requests_mock.last_request.qs == {}

    def test_list_watched_addresses_with_filters(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(
            f"{host}/api/v1/watched-addresses",
            json=[],
        )

        client.list_watched_addresses(chain="STELLAR", enabled=True)

        assert requests_mock.last_request.qs == {
            "chain": ["stellar"],
            "enabled": ["true"],
        }

    def test_list_watched_addresses_enabled_false(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(f"{host}/api/v1/watched-addresses", json=[])

        client.list_watched_addresses(enabled=False)

        assert requests_mock.last_request.qs == {"enabled": ["false"]}

    def test_get_watched_address(self, requests_mock):
        client = SensorServiceClient(host, logger)
        address_id = "29147822-396e-4817-9b64-931c92a05f46"
        requests_mock.get(
            f"{host}/api/v1/watched-addresses/{address_id}",
            json={"id": address_id},
        )

        response = client.get_watched_address(address_id)

        assert response.status_code == 200
        assert response.json()["id"] == address_id

    def test_create_watched_address(self, requests_mock):
        client = SensorServiceClient(host, logger)
        request = CreateWatchedAddressRequest(
            chain=Chain.STELLAR,
            address="GABCDEFGHIJKLMN",
            label="treasury",
            enrichment_strategy=EnrichmentStrategy.MEMO,
            dispatch_topic="LEDGER_TRANSACTION_PAYMENT",
            payload_source="STELLAR_PAYMENT",
            created_by="urn:usrp:admin",
        )
        requests_mock.post(
            f"{host}/api/v1/watched-addresses",
            json={"id": "new-id"},
            status_code=201,
        )

        response = client.create_watched_address(request)

        assert response.status_code == 201
        body = json.loads(requests_mock.last_request.text)
        # excludes None fields
        assert "enabled" not in body
        assert "token_filter" not in body
        assert "max_dispatch_retries" not in body
        assert body["chain"] == "STELLAR"
        assert body["label"] == "treasury"
        assert body["enrichment_strategy"] == "MEMO"
        assert body["dispatch_topic"] == "LEDGER_TRANSACTION_PAYMENT"
        assert body["payload_source"] == "STELLAR_PAYMENT"
        assert body["created_by"] == "urn:usrp:admin"

    def test_update_watched_address(self, requests_mock):
        client = SensorServiceClient(host, logger)
        address_id = "abc-123"
        request = UpdateWatchedAddressRequest(
            enabled=False,
            label="new-label",
        )
        requests_mock.patch(
            f"{host}/api/v1/watched-addresses/{address_id}",
            json={"id": address_id, "enabled": False, "label": "new-label"},
        )

        response = client.update_watched_address(address_id, request)

        assert response.status_code == 200
        body = json.loads(requests_mock.last_request.text)
        assert body == {"enabled": False, "label": "new-label"}

    def test_delete_watched_address(self, requests_mock):
        client = SensorServiceClient(host, logger)
        address_id = "abc-123"
        requests_mock.delete(
            f"{host}/api/v1/watched-addresses/{address_id}",
            status_code=204,
        )

        response = client.delete_watched_address(address_id)

        assert response.status_code == 204

    def test_list_chain_transactions_with_filters(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(f"{host}/api/v1/transactions", json=[])

        client.list_chain_transactions(
            chain="SOLANA",
            status="DISPATCHED",
            recipient="B2JAtKctzWLt4cegWpqBjRqABZDxSSBCNCXPP7Kyk24J",
            limit=50,
        )

        qs = requests_mock.last_request.qs
        assert qs["chain"] == ["solana"]
        assert qs["status"] == ["dispatched"]
        assert qs["recipient"] == ["b2jatkctzwlt4cegwpqbjrqabzdxssbcncxpp7kyk24j"]
        assert qs["limit"] == ["50"]

    def test_get_chain_transaction(self, requests_mock):
        client = SensorServiceClient(host, logger)
        tx_id = "tx-1"
        requests_mock.get(
            f"{host}/api/v1/transactions/{tx_id}",
            json={"id": tx_id},
        )

        response = client.get_chain_transaction(tx_id)

        assert response.status_code == 200
        assert response.json()["id"] == tx_id

    def test_list_intents_with_filters(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(f"{host}/api/v1/intents", json=[])

        client.list_intents(chain="BASE", matched=False, limit=10)

        qs = requests_mock.last_request.qs
        assert qs["chain"] == ["base"]
        assert qs["matched"] == ["false"]
        assert qs["limit"] == ["10"]

    def test_get_intent(self, requests_mock):
        client = SensorServiceClient(host, logger)
        intent_id = "intent-1"
        requests_mock.get(
            f"{host}/api/v1/intents/{intent_id}",
            json={"id": intent_id},
        )

        response = client.get_intent(intent_id)

        assert response.status_code == 200
        assert response.json()["id"] == intent_id

    def test_raises_for_status_on_error(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(
            f"{host}/api/v1/watched-addresses/missing",
            status_code=500,
        )

        with pytest.raises(HTTPError):
            client.get_watched_address("missing")

    def test_authorization_header_when_token_provided(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(f"{host}/api/v1/intents/i-1", json={"id": "i-1"})

        client.get_intent("i-1", token=test_token)

        assert (
            requests_mock.last_request.headers["Authorization"]
            == f"Bearer {test_token.token}"
        )
        assert requests_mock.last_request.headers["User-Agent"] == test_token.subject_id

    def test_no_authorization_header_when_token_omitted(self, requests_mock):
        client = SensorServiceClient(host, logger)
        requests_mock.get(f"{host}/api/v1/intents/i-1", json={"id": "i-1"})

        client.get_intent("i-1")

        assert "Authorization" not in requests_mock.last_request.headers

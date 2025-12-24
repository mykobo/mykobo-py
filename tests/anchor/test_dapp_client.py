import pytest
import logging
from mykobo_py.anchor.dapp.anchor import DappAnchorClient
from mykobo_py.anchor.dapp.models import Transaction


logger = logging.getLogger("test")
host = "https://test-anchor.example.com"


class TestDappAnchorClient:
    """Tests for SolanaAnchorClient"""

    def test_client_initialization(self):
        """Test initializing SolanaAnchorClient"""
        client = DappAnchorClient(host, logger)
        assert client.host == host
        assert client.logger == logger

    def test_make_request_success(self, requests_mock):
        """Test making a successful JSON-RPC request"""
        client = DappAnchorClient(host, logger)

        mock_response = [
            {
                "jsonrpc": "2.0",
                "id": "123",
                "result": {"status": "success"}
            }
        ]

        requests_mock.post(host, json=mock_response)

        result = client.make_request("test_method", {"param": "value"})

        assert result == mock_response
        assert requests_mock.called
        assert requests_mock.call_count == 1

    def test_make_request_failure(self, requests_mock):
        """Test handling request failure"""
        client = DappAnchorClient(host, logger)

        requests_mock.post(host, exc=Exception("Connection error"))

        result = client.make_request("test_method", {"param": "value"})

        assert result is None

    def test_get_transaction_success(self, requests_mock):
        """Test getting a transaction successfully"""
        client = DappAnchorClient(host, logger)
        transaction_id = "29147822-396e-4817-9b64-931c92a05f46"

        mock_transaction_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "Kwabena",
            "id": transaction_id,
            "idempotency_key": "e1d3bdea-77e0-4f18-9c30-a7569b1e3c6f",
            "incoming_currency": "EUR",
            "last_name": "Aning",
            "message_id": "888ce30a-b5b1-4aff-9ff1-5be91c2e3c6f",
            "outgoing_currency": "EURC",
            "payee_id": None,
            "payer_id": "urn:usrp:a891c5585c604b7aa2fd77410d5dc8dc",
            "queue_sent_at": "2025-11-17T20:10:29.960538+00:00",
            "reference": "MYK1763410229",
            "source": "ANCHOR_SOLANA",
            "status": "PENDING_ANCHOR",
            "transaction_type": "DEPOSIT",
            "tx_hash": None,
            "updated_at": "2025-11-17T20:10:29.962143+00:00",
            "value": "20.000000",
            "wallet_address": "B2JAtKctzWLt4cegWpqBjRqABZDxSSBCNCXPP7Kyk24J"
        }

        requests_mock.get(
            f"{host}/api/transaction/{transaction_id}",
            json=mock_transaction_data
        )

        transaction = client.get_transaction(transaction_id)

        assert transaction is not None
        assert isinstance(transaction, Transaction)
        assert transaction.id == transaction_id
        assert transaction.first_name == "Kwabena"
        assert transaction.last_name == "Aning"
        assert transaction.status == "PENDING_ANCHOR"
        assert transaction.transaction_type == "DEPOSIT"
        assert transaction.reference == "MYK1763410229"

    def test_get_transaction_not_found(self, requests_mock):
        """Test getting a transaction that doesn't exist"""
        client = DappAnchorClient(host, logger)
        transaction_id = "non-existent-id"

        requests_mock.get(
            f"{host}/api/transaction/{transaction_id}",
            status_code=404
        )

        transaction = client.get_transaction(transaction_id)

        assert transaction is None

    def test_get_transaction_server_error(self, requests_mock):
        """Test handling server error when getting transaction"""
        client = DappAnchorClient(host, logger)
        transaction_id = "test-id"

        requests_mock.get(
            f"{host}/api/transaction/{transaction_id}",
            status_code=500
        )

        transaction = client.get_transaction(transaction_id)

        assert transaction is None

    def test_get_transaction_exception(self, requests_mock):
        """Test handling exception when getting transaction"""
        client = DappAnchorClient(host, logger)
        transaction_id = "test-id"

        requests_mock.get(
            f"{host}/api/transaction/{transaction_id}",
            exc=Exception("Network error")
        )

        transaction = client.get_transaction(transaction_id)

        assert transaction is None

    def test_make_request_payload_format(self, requests_mock):
        """Test that make_request sends properly formatted JSON-RPC payload"""
        client = DappAnchorClient(host, logger)

        def check_request(request, context):
            payload = request.json()
            assert isinstance(payload, list)
            assert len(payload) == 1
            assert payload[0]["jsonrpc"] == "2.0"
            assert "id" in payload[0]
            assert payload[0]["method"] == "test_method"
            assert payload[0]["params"] == {"key": "value"}
            return [{"jsonrpc": "2.0", "id": payload[0]["id"], "result": {}}]

        requests_mock.post(host, json=check_request)

        client.make_request("test_method", {"key": "value"})

        assert requests_mock.called

    def test_get_transaction_with_completed_status(self, requests_mock):
        """Test getting a completed transaction with tx_hash"""
        client = DappAnchorClient(host, logger)
        transaction_id = "completed-tx-id"

        mock_transaction_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "John",
            "id": transaction_id,
            "idempotency_key": "test-key",
            "incoming_currency": "EUR",
            "last_name": "Doe",
            "message_id": "msg-id",
            "outgoing_currency": "EURC",
            "payee_id": "payee-123",
            "payer_id": "payer-123",
            "queue_sent_at": "2025-11-17T20:10:29.960538+00:00",
            "reference": "REF123",
            "source": "ANCHOR_SOLANA",
            "status": "COMPLETED",
            "transaction_type": "WITHDRAWAL",
            "tx_hash": "5YNmS1R9nNSCDzYx6H9FGqPM4SXNqD6sNgD3KL8XvW7P",
            "updated_at": "2025-11-17T20:15:00.000000+00:00",
            "value": "100.000000",
            "wallet_address": "B2JAtKctzWLt4cegWpqBjRqABZDxSSBCNCXPP7Kyk24J"
        }

        requests_mock.get(
            f"{host}/api/transaction/{transaction_id}",
            json=mock_transaction_data
        )

        transaction = client.get_transaction(transaction_id)

        assert transaction is not None
        assert transaction.status == "COMPLETED"
        assert transaction.tx_hash == "5YNmS1R9nNSCDzYx6H9FGqPM4SXNqD6sNgD3KL8XvW7P"
        assert transaction.has_tx_hash is True
        assert transaction.is_withdrawal is True

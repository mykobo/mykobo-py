import pytest
import json
from mykobo_py.anchor.solana.models import Transaction


class TestTransaction:
    """Tests for Solana Transaction model"""

    def test_transaction_from_json(self):
        """Test deserializing Transaction from JSON"""
        json_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "Kwabena",
            "id": "29147822-396e-4817-9b64-931c92a05f46",
            "idempotency_key": "e1d3bdea-77e0-4f18-9c30-a7569b1e3c6f",
            "incoming_currency": "EUR",
            "last_name": "Aning",
            "message_id": "888ce30a-b5b1-4aff-9ff1-5be91c2e5f07",
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

        transaction = Transaction.from_json(json_data)

        assert transaction.id == "29147822-396e-4817-9b64-931c92a05f46"
        assert transaction.first_name == "Kwabena"
        assert transaction.last_name == "Aning"
        assert transaction.fee == "0.250000"
        assert transaction.value == "20.000000"
        assert transaction.incoming_currency == "EUR"
        assert transaction.outgoing_currency == "EURC"
        assert transaction.status == "PENDING_ANCHOR"
        assert transaction.transaction_type == "DEPOSIT"
        assert transaction.reference == "MYK1763410229"
        assert transaction.source == "ANCHOR_SOLANA"
        assert transaction.wallet_address == "B2JAtKctzWLt4cegWpqBjRqABZDxSSBCNCXPP7Kyk24J"
        assert transaction.payer_id == "urn:usrp:a891c5585c604b7aa2fd77410d5dc8dc"
        assert transaction.payee_id is None
        assert transaction.tx_hash is None

    def test_transaction_with_tx_hash(self):
        """Test Transaction with tx_hash present"""
        json_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "John",
            "id": "test-id-123",
            "idempotency_key": "test-key-123",
            "incoming_currency": "EUR",
            "last_name": "Doe",
            "message_id": "msg-123",
            "outgoing_currency": "EURC",
            "payee_id": "payee-123",
            "payer_id": "payer-123",
            "queue_sent_at": "2025-11-17T20:10:29.960538+00:00",
            "reference": "REF123",
            "source": "ANCHOR_SOLANA",
            "status": "COMPLETED",
            "transaction_type": "WITHDRAWAL",
            "tx_hash": "5YNmS1R9nNSCDzYx6H9FGqPM4SXNqD6sNgD3KL8XvW7P",
            "updated_at": "2025-11-17T20:10:29.962143+00:00",
            "value": "100.000000",
            "wallet_address": "B2JAtKctzWLt4cegWpqBjRqABZDxSSBCNCXPP7Kyk24J"
        }

        transaction = Transaction.from_json(json_data)

        assert transaction.tx_hash == "5YNmS1R9nNSCDzYx6H9FGqPM4SXNqD6sNgD3KL8XvW7P"
        assert transaction.payee_id == "payee-123"
        assert transaction.transaction_type == "WITHDRAWAL"
        assert transaction.status == "COMPLETED"

    def test_is_pending_anchor_property(self):
        """Test is_pending_anchor property"""
        json_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "Test",
            "id": "test-id",
            "idempotency_key": "test-key",
            "incoming_currency": "EUR",
            "last_name": "User",
            "message_id": "msg-id",
            "outgoing_currency": "EURC",
            "payee_id": None,
            "payer_id": "payer-id",
            "queue_sent_at": "2025-11-17T20:10:29.960538+00:00",
            "reference": "REF123",
            "source": "ANCHOR_SOLANA",
            "status": "PENDING_ANCHOR",
            "transaction_type": "DEPOSIT",
            "tx_hash": None,
            "updated_at": "2025-11-17T20:10:29.962143+00:00",
            "value": "50.000000",
            "wallet_address": "wallet-addr"
        }

        transaction = Transaction.from_json(json_data)
        assert transaction.is_pending_anchor is True

        json_data["status"] = "COMPLETED"
        transaction = Transaction.from_json(json_data)
        assert transaction.is_pending_anchor is False

    def test_is_deposit_property(self):
        """Test is_deposit property"""
        json_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "Test",
            "id": "test-id",
            "idempotency_key": "test-key",
            "incoming_currency": "EUR",
            "last_name": "User",
            "message_id": "msg-id",
            "outgoing_currency": "EURC",
            "payee_id": None,
            "payer_id": "payer-id",
            "queue_sent_at": "2025-11-17T20:10:29.960538+00:00",
            "reference": "REF123",
            "source": "ANCHOR_SOLANA",
            "status": "PENDING_ANCHOR",
            "transaction_type": "DEPOSIT",
            "tx_hash": None,
            "updated_at": "2025-11-17T20:10:29.962143+00:00",
            "value": "50.000000",
            "wallet_address": "wallet-addr"
        }

        transaction = Transaction.from_json(json_data)
        assert transaction.is_deposit is True
        assert transaction.is_withdrawal is False

    def test_is_withdrawal_property(self):
        """Test is_withdrawal property"""
        json_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "Test",
            "id": "test-id",
            "idempotency_key": "test-key",
            "incoming_currency": "EUR",
            "last_name": "User",
            "message_id": "msg-id",
            "outgoing_currency": "EURC",
            "payee_id": None,
            "payer_id": "payer-id",
            "queue_sent_at": "2025-11-17T20:10:29.960538+00:00",
            "reference": "REF123",
            "source": "ANCHOR_SOLANA",
            "status": "PENDING_ANCHOR",
            "transaction_type": "WITHDRAWAL",
            "tx_hash": None,
            "updated_at": "2025-11-17T20:10:29.962143+00:00",
            "value": "50.000000",
            "wallet_address": "wallet-addr"
        }

        transaction = Transaction.from_json(json_data)
        assert transaction.is_withdrawal is True
        assert transaction.is_deposit is False

    def test_has_tx_hash_property(self):
        """Test has_tx_hash property"""
        json_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "Test",
            "id": "test-id",
            "idempotency_key": "test-key",
            "incoming_currency": "EUR",
            "last_name": "User",
            "message_id": "msg-id",
            "outgoing_currency": "EURC",
            "payee_id": None,
            "payer_id": "payer-id",
            "queue_sent_at": "2025-11-17T20:10:29.960538+00:00",
            "reference": "REF123",
            "source": "ANCHOR_SOLANA",
            "status": "COMPLETED",
            "transaction_type": "DEPOSIT",
            "tx_hash": "5YNmS1R9nNSCDzYx6H9FGqPM4SXNqD6sNgD3KL8XvW7P",
            "updated_at": "2025-11-17T20:10:29.962143+00:00",
            "value": "50.000000",
            "wallet_address": "wallet-addr"
        }

        transaction = Transaction.from_json(json_data)
        assert transaction.has_tx_hash is True

        json_data["tx_hash"] = None
        transaction = Transaction.from_json(json_data)
        assert transaction.has_tx_hash is False

        json_data["tx_hash"] = ""
        transaction = Transaction.from_json(json_data)
        assert transaction.has_tx_hash is False

    def test_transaction_dict_method(self):
        """Test converting Transaction to dict"""
        json_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "Kwabena",
            "id": "29147822-396e-4817-9b64-931c92a05f46",
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

        transaction = Transaction.from_json(json_data)
        result_dict = transaction.dict()

        assert isinstance(result_dict, dict)
        assert result_dict["id"] == "29147822-396e-4817-9b64-931c92a05f46"
        assert result_dict["first_name"] == "Kwabena"
        assert result_dict["value"] == "20.000000"
        assert result_dict["tx_hash"] is None
        assert result_dict["payee_id"] is None

    def test_transaction_missing_fields_default_to_empty(self):
        """Test that missing fields default to appropriate values"""
        minimal_json = {
            "id": "test-id",
            "reference": "REF123"
        }

        transaction = Transaction.from_json(minimal_json)

        assert transaction.id == "test-id"
        assert transaction.reference == "REF123"
        assert transaction.fee == "0"
        assert transaction.value == "0"
        assert transaction.first_name == ""
        assert transaction.last_name == ""
        assert transaction.tx_hash is None
        assert transaction.payee_id is None

import pytest
import json
import os
from mykobo_py.anchor.dapp.models import Transaction


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

    def test_transaction_from_payload_file(self):
        """Test loading transaction from the transaction-payload.json file"""
        payload_file = os.path.join(os.path.dirname(__file__), "transaction-payload.json")

        with open(payload_file, 'r') as f:
            json_data = json.load(f)

        transaction = Transaction.from_json(json_data)

        # Verify basic fields
        assert transaction.id == "3b40bc2a-9cc9-420b-a595-1b4d89ae169c"
        assert transaction.first_name == "Kwabena"
        assert transaction.last_name == "Aning"
        assert transaction.value == "2.000000"
        assert transaction.fee == "0.030000"
        assert transaction.status == "PENDING_RAMP"
        assert transaction.transaction_type == "WITHDRAW"
        assert transaction.reference == "MYK1766360012"

        # Special attention to network field
        assert transaction.network == "stellar"
        assert transaction.network is not None

        # Special attention to client_domain field
        assert transaction.client_domain == "stellar.mykobo.app"
        assert transaction.client_domain is not None

        # Special attention to comment field (null in this case)
        assert transaction.comment is None

        # Verify other fields specific to this payload
        assert transaction.tx_hash == "2c87dfe7387c3156c988215dbc0a10ddc8cc97f4c9bd1a430a5aeb6335645a02"
        assert transaction.wallet_address == "GDFDQ6QNTNUQK2NPLM3QLW73LAZ7FX6WXKWHQTLL47IKFTT3T7PRY34T"
        assert transaction.source == "ANCHOR_DAPP"

    def test_transaction_with_network_field(self):
        """Test transaction with network field set to different values"""
        # Test with stellar network
        stellar_data = {
            "id": "test-id-stellar",
            "reference": "REF-STELLAR",
            "network": "stellar",
            "wallet_address": "GDFDQ6QNTNUQK2NPLM3QLW73LAZ7FX6WXKWHQTLL47IKFTT3T7PRY34T",
            "tx_hash": "stellar-hash-123"
        }

        transaction = Transaction.from_json(stellar_data)
        assert transaction.network == "stellar"
        assert transaction.wallet_address == "GDFDQ6QNTNUQK2NPLM3QLW73LAZ7FX6WXKWHQTLL47IKFTT3T7PRY34T"

        # Test with solana network
        solana_data = {
            "id": "test-id-solana",
            "reference": "REF-SOLANA",
            "network": "solana",
            "wallet_address": "B2JAtKctzWLt4cegWpqBjRqABZDxSSBCNCXPP7Kyk24J",
            "tx_hash": "solana-hash-456"
        }

        transaction = Transaction.from_json(solana_data)
        assert transaction.network == "solana"
        assert transaction.wallet_address == "B2JAtKctzWLt4cegWpqBjRqABZDxSSBCNCXPP7Kyk24J"

        # Test with ethereum network
        ethereum_data = {
            "id": "test-id-ethereum",
            "reference": "REF-ETH",
            "network": "ethereum",
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        }

        transaction = Transaction.from_json(ethereum_data)
        assert transaction.network == "ethereum"

    def test_transaction_with_client_domain_field(self):
        """Test transaction with client_domain field"""
        # Test with stellar.mykobo.app
        stellar_domain_data = {
            "id": "test-id-1",
            "reference": "REF-1",
            "client_domain": "stellar.mykobo.app",
            "network": "stellar"
        }

        transaction = Transaction.from_json(stellar_domain_data)
        assert transaction.client_domain == "stellar.mykobo.app"

        # Test with different domain
        solana_domain_data = {
            "id": "test-id-2",
            "reference": "REF-2",
            "client_domain": "solana.mykobo.app",
            "network": "solana"
        }

        transaction = Transaction.from_json(solana_domain_data)
        assert transaction.client_domain == "solana.mykobo.app"

        # Test with custom domain
        custom_domain_data = {
            "id": "test-id-3",
            "reference": "REF-3",
            "client_domain": "custom.example.com",
            "network": "stellar"
        }

        transaction = Transaction.from_json(custom_domain_data)
        assert transaction.client_domain == "custom.example.com"

    def test_transaction_with_comment_null(self):
        """Test transaction with comment field set to null"""
        json_data = {
            "id": "test-id-comment-null",
            "reference": "REF-COMMENT-NULL",
            "comment": None,
            "network": "stellar",
            "client_domain": "stellar.mykobo.app"
        }

        transaction = Transaction.from_json(json_data)
        assert transaction.comment is None

    def test_transaction_with_comment_value(self):
        """Test transaction with comment field containing a string value"""
        # Test with simple comment
        json_data_1 = {
            "id": "test-id-comment-1",
            "reference": "REF-COMMENT-1",
            "comment": "Payment for invoice #12345",
            "network": "stellar",
            "client_domain": "stellar.mykobo.app"
        }

        transaction = Transaction.from_json(json_data_1)
        assert transaction.comment == "Payment for invoice #12345"
        assert transaction.comment is not None

        # Test with longer comment
        json_data_2 = {
            "id": "test-id-comment-2",
            "reference": "REF-COMMENT-2",
            "comment": "This is a longer comment with special characters: @#$% and unicode émojis 🚀",
            "network": "solana"
        }

        transaction = Transaction.from_json(json_data_2)
        assert transaction.comment == "This is a longer comment with special characters: @#$% and unicode émojis 🚀"

        # Test with empty string comment
        json_data_3 = {
            "id": "test-id-comment-3",
            "reference": "REF-COMMENT-3",
            "comment": "",
            "network": "stellar"
        }

        transaction = Transaction.from_json(json_data_3)
        assert transaction.comment == ""

    def test_transaction_new_fields_in_dict_method(self):
        """Test that network, client_domain, and comment are included in dict() output"""
        json_data = {
            "id": "test-id-dict",
            "reference": "REF-DICT",
            "network": "stellar",
            "client_domain": "stellar.mykobo.app",
            "comment": "Test comment for dict method",
            "created_at": "2025-12-21T23:33:33.122548+00:00",
            "fee": "0.030000",
            "first_name": "Test",
            "last_name": "User",
            "idempotency_key": "test-key",
            "incoming_currency": "EURC",
            "message_id": "msg-id",
            "outgoing_currency": "EUR",
            "payee_id": "payee-123",
            "payer_id": "payer-123",
            "queue_sent_at": "2025-12-21T23:33:33.794990+00:00",
            "source": "ANCHOR_DAPP",
            "status": "PENDING_RAMP",
            "transaction_type": "WITHDRAW",
            "tx_hash": "test-hash",
            "updated_at": "2025-12-22T00:38:52.143581+00:00",
            "value": "2.000000",
            "wallet_address": "test-wallet"
        }

        transaction = Transaction.from_json(json_data)
        result_dict = transaction.dict()

        # Verify new fields are present in dict output
        assert "network" in result_dict
        assert result_dict["network"] == "stellar"

        assert "client_domain" in result_dict
        assert result_dict["client_domain"] == "stellar.mykobo.app"

        assert "comment" in result_dict
        assert result_dict["comment"] == "Test comment for dict method"

    def test_transaction_new_fields_with_null_in_dict(self):
        """Test that null values for network, client_domain, and comment are preserved in dict()"""
        json_data = {
            "id": "test-id-null-dict",
            "reference": "REF-NULL-DICT",
            "network": None,
            "client_domain": None,
            "comment": None
        }

        transaction = Transaction.from_json(json_data)
        result_dict = transaction.dict()

        # Verify null values are preserved
        assert result_dict["network"] is None
        assert result_dict["client_domain"] is None
        assert result_dict["comment"] is None

    def test_transaction_backwards_compatibility_without_new_fields(self):
        """Test that transactions without network, client_domain, and comment still work"""
        # Old transaction format without new fields
        old_json_data = {
            "created_at": "2025-11-17T20:10:29.815872+00:00",
            "fee": "0.250000",
            "first_name": "Legacy",
            "id": "legacy-id",
            "idempotency_key": "legacy-key",
            "incoming_currency": "EUR",
            "last_name": "User",
            "message_id": "legacy-msg",
            "outgoing_currency": "EURC",
            "payee_id": None,
            "payer_id": "legacy-payer",
            "queue_sent_at": "2025-11-17T20:10:29.960538+00:00",
            "reference": "LEGACY-REF",
            "source": "ANCHOR_SOLANA",
            "status": "COMPLETED",
            "transaction_type": "DEPOSIT",
            "tx_hash": "legacy-hash",
            "updated_at": "2025-11-17T20:10:29.962143+00:00",
            "value": "100.000000",
            "wallet_address": "legacy-wallet"
        }

        transaction = Transaction.from_json(old_json_data)

        # Verify basic fields work
        assert transaction.id == "legacy-id"
        assert transaction.first_name == "Legacy"
        assert transaction.value == "100.000000"

        # Verify new fields default to None when not present
        assert transaction.network is None
        assert transaction.client_domain is None
        assert transaction.comment is None

        # Verify dict() method works
        result_dict = transaction.dict()
        assert result_dict["id"] == "legacy-id"
        assert result_dict["network"] is None
        assert result_dict["client_domain"] is None
        assert result_dict["comment"] is None

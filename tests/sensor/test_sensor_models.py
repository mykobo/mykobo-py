from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

import pytest

from mykobo_py.sensor.models.common import (
    Chain,
    EnrichmentStrategy,
    TransactionStatus,
)
from mykobo_py.sensor.models.response import (
    ChainTransaction,
    Intent,
    WatchedAddress,
)


class TestWatchedAddress:
    def test_from_json(self):
        payload = {
            "id": "29147822-396e-4817-9b64-931c92a05f46",
            "chain": "STELLAR",
            "address": "GABCDEFGHIJKLMN",
            "label": "treasury",
            "enabled": True,
            "token_filter": ["USDC", "EURC"],
            "enrichment_strategy": "INTENT_MATCH",
            "dispatch_topic": "LEDGER_TRANSACTION_PAYMENT",
            "payload_source": "STELLAR_PAYMENT",
            "max_dispatch_retries": 5,
            "created_by": "urn:usrp:admin",
            "created_at": "2026-01-10T10:00:00+00:00",
            "updated_at": "2026-01-11T11:00:00+00:00",
        }

        wa = WatchedAddress.model_validate(payload)

        assert wa.id == UUID("29147822-396e-4817-9b64-931c92a05f46")
        assert wa.chain is Chain.STELLAR
        assert wa.address == "GABCDEFGHIJKLMN"
        assert wa.label == "treasury"
        assert wa.enabled is True
        assert wa.token_filter == ["USDC", "EURC"]
        assert wa.enrichment_strategy is EnrichmentStrategy.INTENT_MATCH
        assert wa.dispatch_topic == "LEDGER_TRANSACTION_PAYMENT"
        assert wa.payload_source == "STELLAR_PAYMENT"
        assert wa.max_dispatch_retries == 5
        assert wa.created_by == "urn:usrp:admin"
        assert wa.created_at == datetime(2026, 1, 10, 10, 0, tzinfo=timezone.utc)
        assert wa.updated_at == datetime(2026, 1, 11, 11, 0, tzinfo=timezone.utc)


class TestChainTransaction:
    def test_minimal_payload(self):
        payload = {
            "id": "9e2f8c41-1b3a-4b9e-9c0d-1234567890ab",
            "chain": "SOLANA",
            "tx_hash": "5YNmS1R9nNSCDzYx6H9FGqPM4SXNqD6sNgD3KL8XvW7P",
            "sender": "sender-addr",
            "recipient": "recipient-addr",
            "amount": "100.000000",
            "token": "USDC",
            "status": "RECEIVED",
            "dispatch_retries": 0,
            "received_at": "2026-04-01T12:00:00+00:00",
        }

        ct = ChainTransaction.model_validate(payload)

        assert ct.id == UUID("9e2f8c41-1b3a-4b9e-9c0d-1234567890ab")
        assert ct.chain is Chain.SOLANA
        assert ct.amount == Decimal("100.000000")
        assert ct.status is TransactionStatus.RECEIVED
        assert ct.block_number is None
        assert ct.memo is None
        assert ct.failure_reason is None
        assert ct.raw_data is None
        assert ct.dispatched_at is None

    def test_full_payload_preserves_decimal_precision(self):
        payload = {
            "id": "9e2f8c41-1b3a-4b9e-9c0d-1234567890ab",
            "chain": "BASE",
            "tx_hash": "0xabc",
            "sender": "0xsender",
            "recipient": "0xrecipient",
            "amount": "0.123456789012345678",
            "token": "USDC",
            "block_number": 42_000_000,
            "memo": "MYK-REF-1",
            "status": "DISPATCHED",
            "dispatch_retries": 2,
            "failure_reason": None,
            "raw_data": {"logs": ["a", "b"], "value": 1},
            "received_at": "2026-04-01T12:00:00+00:00",
            "dispatched_at": "2026-04-01T12:00:05+00:00",
        }

        ct = ChainTransaction.model_validate(payload)

        assert ct.amount == Decimal("0.123456789012345678")
        assert ct.block_number == 42_000_000
        assert ct.memo == "MYK-REF-1"
        assert ct.status is TransactionStatus.DISPATCHED
        assert ct.dispatch_retries == 2
        assert ct.raw_data == {"logs": ["a", "b"], "value": 1}
        assert ct.dispatched_at == datetime(2026, 4, 1, 12, 0, 5, tzinfo=timezone.utc)


class TestIntent:
    def _base_payload(self):
        return {
            "id": "11111111-1111-1111-1111-111111111111",
            "chain": "STELLAR",
            "target_address": "GTARGET",
            "expected_sender": "GSENDER",
            "expected_amount": "25.500000",
            "expected_token": "EURC",
            "reference": "MYK1763410229",
            "source": "DAPP",
            "matched": False,
            "expires_at": "2026-04-01T13:00:00+00:00",
            "created_at": "2026-04-01T12:00:00+00:00",
        }

    def test_unmatched(self):
        intent = Intent.model_validate(self._base_payload())

        assert intent.matched is False
        assert intent.chain_transaction_id is None
        assert intent.expected_amount == Decimal("25.500000")

    def test_matched(self):
        payload = self._base_payload()
        payload["matched"] = True
        payload["chain_transaction_id"] = "22222222-2222-2222-2222-222222222222"

        intent = Intent.model_validate(payload)

        assert intent.matched is True
        assert intent.chain_transaction_id == UUID(
            "22222222-2222-2222-2222-222222222222"
        )


class TestEnums:
    @pytest.mark.parametrize("value", ["STELLAR", "SOLANA", "BASE"])
    def test_chain_values(self, value):
        assert Chain(value).value == value

    @pytest.mark.parametrize("value", ["RECEIVED", "DISPATCHED", "FAILED"])
    def test_transaction_status_values(self, value):
        assert TransactionStatus(value).value == value

    @pytest.mark.parametrize("value", ["MEMO", "INTENT_MATCH"])
    def test_enrichment_strategy_values(self, value):
        assert EnrichmentStrategy(value).value == value

import pytest
from pydantic import ValidationError

from mykobo_py.message_bus.models.notification import (
    CustomerNotificationPayload,
    PlatformNotificationPayload,
    ProfileSubject,
    RelaySubject,
    Severity,
    TransactionSubject,
)


def test_severity_values():
    assert Severity.INFO.value == "info"
    assert Severity.WARNING.value == "warning"
    assert Severity.CRITICAL.value == "critical"


def test_severity_ordering():
    assert Severity.INFO < Severity.WARNING < Severity.CRITICAL
    assert Severity.CRITICAL > Severity.INFO
    assert Severity.WARNING >= Severity.WARNING


def test_relay_subject_serializes_with_discriminator():
    s = RelaySubject(id="abc-123", source_chain="stellar", destination_chain="solana")
    assert s.model_dump(exclude_none=True) == {
        "type": "relay",
        "id": "abc-123",
        "source_chain": "stellar",
        "destination_chain": "solana",
    }


def test_transaction_subject_serializes():
    s = TransactionSubject(reference="ref-1")
    assert s.model_dump(exclude_none=True) == {"type": "transaction", "reference": "ref-1"}


def test_profile_subject_serializes():
    s = ProfileSubject(user_id="u-1")
    assert s.model_dump(exclude_none=True) == {"type": "profile", "user_id": "u-1"}


def test_subject_missing_required_field_rejected():
    with pytest.raises((ValidationError, ValueError)):
        RelaySubject(id="", source_chain="stellar", destination_chain="solana")


def test_customer_payload_carries_subject_and_data():
    p = CustomerNotificationPayload(
        subject=RelaySubject(id="abc", source_chain="stellar", destination_chain="solana"),
        data={"email": "u@e.com", "amount": "100"},
    )
    d = p.to_dict()  # inherited from Payload
    assert d["subject"]["type"] == "relay"
    assert d["data"] == {"email": "u@e.com", "amount": "100"}


def test_platform_payload_with_subject():
    p = PlatformNotificationPayload(
        severity=Severity.WARNING,
        data={"k": "v"},
        subject="relay:abc",
    )
    d = p.to_dict()
    assert d == {"severity": "warning", "data": {"k": "v"}, "subject": "relay:abc"}


def test_platform_payload_without_subject_excludes_none():
    p = PlatformNotificationPayload(severity=Severity.CRITICAL, data={"k": "v"})
    d = p.to_dict()
    assert "subject" not in d  # exclude_none=True drops it
    assert d == {"severity": "critical", "data": {"k": "v"}}


def test_customer_subject_discriminated_union_round_trip():
    # Deserializing back into the right subject type
    raw = {"type": "transaction", "reference": "ref-1"}
    s = TransactionSubject.model_validate(raw)
    assert isinstance(s, TransactionSubject)
    assert s.reference == "ref-1"

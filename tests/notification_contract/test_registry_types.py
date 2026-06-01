import pytest

from mykobo_py.message_bus.models.base import EventType
from mykobo_py.notification_contract.predicates import Equals
from mykobo_py.notification_contract.registry import (
    Audience,
    DomainEntry,
    NotificationEntry,
    NotificationRule,
    Registry,
    RegistryError,
    Severity,
    VariantKind,
)


def _minimal_data():
    return {
        "version": 1,
        "variants": {
            "NEW_TRANSACTION": {
                "kind": "domain",
                "notifies": [{"fires": ["RELAY_INITIATED"]}],
            },
            "TRANSACTION_STATUS_UPDATE": {
                "kind": "domain",
                "notifies": [
                    {
                        "when": 'status == "FUNDS_RECEIVED"',
                        "fires": ["RELAY_COMPLETED"],
                    }
                ],
            },
            "NEW_BANK_PAYMENT": {
                "kind": "domain",
                "notifies": [],
                "reason": "Internal ingress; user told via downstream rails.",
            },
            "NEW_PROFILE": {
                "kind": "domain",
                "notifies": [{"fires": ["RELAY_INITIATED"]}],
            },
            "NEW_USER": {
                "kind": "domain",
                "notifies": [{"fires": ["RELAY_INITIATED"]}],
            },
            "KYC_EVENT": {
                "kind": "domain",
                "notifies": [],
                "reason": "KYC outcomes surface via dapp idenfy/sumsub callbacks.",
            },
            "ADDRESS_ONBOARDED": {
                "kind": "domain",
                "notifies": [],
                "reason": "Internal indexing event.",
            },
            "RELAY_INITIATED": {"kind": "notification", "audience": "customer"},
            "RELAY_COMPLETED": {"kind": "notification", "audience": "customer"},
            "RELAY_ONBOARDED": {"kind": "notification", "audience": "customer"},
            "RELAY_STUCK_DEPOSITING": {
                "kind": "notification", "audience": "platform", "severity": "warning",
            },
            "RELAY_STUCK_BRIDGING": {
                "kind": "notification", "audience": "platform", "severity": "warning",
            },
            "RELAY_STUCK_FORWARDING": {
                "kind": "notification", "audience": "platform", "severity": "warning",
            },
            "RELAY_FAILED": {
                "kind": "notification", "audience": "platform", "severity": "critical",
            },
            "CIRCLE_API_5XX_BURST": {
                "kind": "notification", "audience": "platform", "severity": "warning",
            },
            "WEBHOOK_REPROCESSOR_BACKLOG": {
                "kind": "notification", "audience": "platform", "severity": "warning",
            },
            "VERIFICATION_REQUESTED": {"kind": "notification", "audience": "customer"},
            "PASSWORD_RESET_REQUESTED": {"kind": "notification", "audience": "customer"},
        },
    }


def test_loads_minimal_registry():
    reg = Registry.from_dict(_minimal_data())
    assert reg.is_notification(EventType.RELAY_INITIATED) is True
    assert reg.is_notification(EventType.NEW_TRANSACTION) is False


def test_audience_of_customer():
    reg = Registry.from_dict(_minimal_data())
    assert reg.audience_of(EventType.RELAY_INITIATED) == Audience.CUSTOMER


def test_audience_of_platform():
    reg = Registry.from_dict(_minimal_data())
    assert reg.audience_of(EventType.RELAY_STUCK_DEPOSITING) == Audience.PLATFORM


def test_severity_of_platform_warning():
    reg = Registry.from_dict(_minimal_data())
    assert reg.severity_of(EventType.RELAY_STUCK_DEPOSITING) == Severity.WARNING


def test_severity_of_customer_none():
    reg = Registry.from_dict(_minimal_data())
    assert reg.severity_of(EventType.RELAY_INITIATED) is None


def test_domain_entry_parsed_predicate():
    reg = Registry.from_dict(_minimal_data())
    entry = reg.entries[EventType.TRANSACTION_STATUS_UPDATE]
    assert isinstance(entry, DomainEntry)
    assert entry.notifies[0].when == Equals("status", "FUNDS_RECEIVED")


def test_missing_enum_variant_raises():
    data = _minimal_data()
    del data["variants"]["NEW_USER"]
    with pytest.raises(RegistryError, match="NEW_USER"):
        Registry.from_dict(data)


def test_extra_yaml_key_raises():
    data = _minimal_data()
    data["variants"]["NOT_A_REAL_VARIANT"] = {"kind": "notification", "audience": "customer"}
    with pytest.raises(RegistryError, match="NOT_A_REAL_VARIANT"):
        Registry.from_dict(data)


def test_empty_notifies_without_reason_raises():
    data = _minimal_data()
    data["variants"]["KYC_EVENT"] = {"kind": "domain", "notifies": []}  # no reason
    with pytest.raises(RegistryError, match="KYC_EVENT.*reason"):
        Registry.from_dict(data)


def test_fires_target_must_be_notification_kind():
    data = _minimal_data()
    data["variants"]["NEW_TRANSACTION"]["notifies"] = [{"fires": ["NEW_USER"]}]
    with pytest.raises(RegistryError, match="NEW_USER.*notification"):
        Registry.from_dict(data)


def test_platform_must_have_severity():
    data = _minimal_data()
    data["variants"]["RELAY_FAILED"] = {"kind": "notification", "audience": "platform"}
    with pytest.raises(RegistryError, match="RELAY_FAILED.*severity"):
        Registry.from_dict(data)


def test_customer_must_not_have_severity():
    data = _minimal_data()
    data["variants"]["RELAY_INITIATED"] = {
        "kind": "notification", "audience": "customer", "severity": "info",
    }
    with pytest.raises(RegistryError, match="RELAY_INITIATED.*severity"):
        Registry.from_dict(data)


def test_version_mismatch_raises():
    data = _minimal_data()
    data["version"] = 99
    with pytest.raises(RegistryError, match="version"):
        Registry.from_dict(data)


def test_notifications_for_unconditional():
    reg = Registry.from_dict(_minimal_data())
    assert reg.notifications_for(EventType.NEW_TRANSACTION, {}) == [EventType.RELAY_INITIATED]


def test_notifications_for_conditional_matches():
    reg = Registry.from_dict(_minimal_data())
    result = reg.notifications_for(
        EventType.TRANSACTION_STATUS_UPDATE, {"status": "FUNDS_RECEIVED"}
    )
    assert result == [EventType.RELAY_COMPLETED]


def test_notifications_for_conditional_no_match():
    reg = Registry.from_dict(_minimal_data())
    result = reg.notifications_for(
        EventType.TRANSACTION_STATUS_UPDATE, {"status": "PENDING"}
    )
    assert result == []


def test_notifications_for_notification_kind_returns_empty():
    reg = Registry.from_dict(_minimal_data())
    assert reg.notifications_for(EventType.RELAY_INITIATED, {}) == []


def test_notifications_for_no_op_for_empty_notifies():
    reg = Registry.from_dict(_minimal_data())
    assert reg.notifications_for(EventType.KYC_EVENT, {}) == []


def test_notifies_must_be_list():
    data = _minimal_data()
    data["variants"]["NEW_TRANSACTION"] = {"kind": "domain", "notifies": "RELAY_INITIATED"}
    with pytest.raises(RegistryError, match="NEW_TRANSACTION.*list"):
        Registry.from_dict(data)


def test_notifies_item_must_be_mapping():
    data = _minimal_data()
    data["variants"]["NEW_TRANSACTION"] = {"kind": "domain", "notifies": ["RELAY_INITIATED"]}
    with pytest.raises(RegistryError, match="NEW_TRANSACTION.*mapping"):
        Registry.from_dict(data)


def test_when_must_be_string():
    data = _minimal_data()
    data["variants"]["TRANSACTION_STATUS_UPDATE"] = {
        "kind": "domain",
        "notifies": [{"when": 42, "fires": ["RELAY_COMPLETED"]}],
    }
    with pytest.raises(RegistryError, match="TRANSACTION_STATUS_UPDATE.*when.*string"):
        Registry.from_dict(data)


def test_fires_unknown_variant_includes_name():
    data = _minimal_data()
    data["variants"]["NEW_TRANSACTION"]["notifies"] = [{"fires": ["NO_SUCH_EVENT"]}]
    with pytest.raises(RegistryError, match="NO_SUCH_EVENT"):
        Registry.from_dict(data)

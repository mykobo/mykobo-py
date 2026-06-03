from mykobo_py.message_bus.models.base import EventType
from mykobo_py.notification_contract import REGISTRY, Audience, Severity


def test_registry_loaded_at_import():
    assert REGISTRY is not None


def test_every_enum_variant_classified():
    classified = set(REGISTRY.entries.keys())
    assert classified == set(EventType)


def test_relay_initiated_is_customer_notification():
    assert REGISTRY.is_notification(EventType.RELAY_INITIATED)
    assert REGISTRY.audience_of(EventType.RELAY_INITIATED) == Audience.CUSTOMER
    assert REGISTRY.severity_of(EventType.RELAY_INITIATED) is None


def test_relay_failed_is_critical_platform_notification():
    assert REGISTRY.is_notification(EventType.RELAY_FAILED)
    assert REGISTRY.audience_of(EventType.RELAY_FAILED) == Audience.PLATFORM
    assert REGISTRY.severity_of(EventType.RELAY_FAILED) == Severity.CRITICAL


def test_new_transaction_is_domain_kind():
    assert REGISTRY.is_notification(EventType.NEW_TRANSACTION) is False
    assert REGISTRY.notifications_for(EventType.NEW_TRANSACTION, {}) == []


def test_kyc_event_no_notification_with_reason():
    entry = REGISTRY.entries[EventType.KYC_EVENT]
    assert entry.notifies == ()
    assert entry.reason is not None
    assert len(entry.reason) > 10


def test_mint_burn_event_variants_exist():
    assert EventType.MINT_COMPLETED.value == "MINT_COMPLETED"
    assert EventType.BURN_COMPLETED.value == "BURN_COMPLETED"
    assert EventType.MINT_HELD.value == "MINT_HELD"
    assert EventType.BURN_HELD.value == "BURN_HELD"
    assert EventType.MINT_HELD_ALERT.value == "MINT_HELD_ALERT"
    assert EventType.BURN_HELD_ALERT.value == "BURN_HELD_ALERT"
    assert EventType.CUSTOMER_NOTIFY_FAILED.value == "CUSTOMER_NOTIFY_FAILED"
    assert EventType.MINT_INFO.value == "MINT_INFO"
    assert EventType.BURN_INFO.value == "BURN_INFO"

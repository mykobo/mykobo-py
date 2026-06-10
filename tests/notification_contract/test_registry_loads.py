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


def test_mint_completed_is_customer_notification():
    assert REGISTRY.is_notification(EventType.MINT_COMPLETED)
    assert REGISTRY.audience_of(EventType.MINT_COMPLETED) == Audience.CUSTOMER
    assert REGISTRY.severity_of(EventType.MINT_COMPLETED) is None


def test_burn_completed_is_platform_info_notification():
    """BURN_COMPLETED is platform-info: the customer-facing withdraw
    lifecycle is told via WITHDRAW_INITIATED / WITHDRAW_COMPLETED, so
    BURN_COMPLETED is an ops-only signal on the slack channel."""
    assert REGISTRY.is_notification(EventType.BURN_COMPLETED)
    assert REGISTRY.audience_of(EventType.BURN_COMPLETED) == Audience.PLATFORM
    assert REGISTRY.severity_of(EventType.BURN_COMPLETED) == Severity.INFO


def test_mint_held_is_customer_notification():
    assert REGISTRY.is_notification(EventType.MINT_HELD)
    assert REGISTRY.audience_of(EventType.MINT_HELD) == Audience.CUSTOMER
    assert REGISTRY.severity_of(EventType.MINT_HELD) is None


def test_burn_held_is_customer_notification():
    assert REGISTRY.is_notification(EventType.BURN_HELD)
    assert REGISTRY.audience_of(EventType.BURN_HELD) == Audience.CUSTOMER
    assert REGISTRY.severity_of(EventType.BURN_HELD) is None


def test_mint_held_alert_is_platform_warning():
    assert REGISTRY.is_notification(EventType.MINT_HELD_ALERT)
    assert REGISTRY.audience_of(EventType.MINT_HELD_ALERT) == Audience.PLATFORM
    assert REGISTRY.severity_of(EventType.MINT_HELD_ALERT) == Severity.WARNING


def test_burn_held_alert_is_platform_warning():
    assert REGISTRY.is_notification(EventType.BURN_HELD_ALERT)
    assert REGISTRY.audience_of(EventType.BURN_HELD_ALERT) == Audience.PLATFORM
    assert REGISTRY.severity_of(EventType.BURN_HELD_ALERT) == Severity.WARNING


def test_customer_notify_failed_is_platform_warning():
    assert REGISTRY.is_notification(EventType.CUSTOMER_NOTIFY_FAILED)
    assert REGISTRY.audience_of(EventType.CUSTOMER_NOTIFY_FAILED) == Audience.PLATFORM
    assert REGISTRY.severity_of(EventType.CUSTOMER_NOTIFY_FAILED) == Severity.WARNING


def test_mint_info_is_platform_info():
    assert REGISTRY.is_notification(EventType.MINT_INFO)
    assert REGISTRY.audience_of(EventType.MINT_INFO) == Audience.PLATFORM
    assert REGISTRY.severity_of(EventType.MINT_INFO) == Severity.INFO


def test_burn_info_is_platform_info():
    assert REGISTRY.is_notification(EventType.BURN_INFO)
    assert REGISTRY.audience_of(EventType.BURN_INFO) == Audience.PLATFORM
    assert REGISTRY.severity_of(EventType.BURN_INFO) == Severity.INFO


def test_customer_funds_received_is_customer_audience():
    assert REGISTRY.is_notification(EventType.CUSTOMER_FUNDS_RECEIVED)
    assert REGISTRY.audience_of(EventType.CUSTOMER_FUNDS_RECEIVED) == Audience.CUSTOMER
    assert REGISTRY.severity_of(EventType.CUSTOMER_FUNDS_RECEIVED) is None


def test_transaction_funded_info_is_platform_info():
    assert REGISTRY.is_notification(EventType.TRANSACTION_FUNDED_INFO)
    assert REGISTRY.audience_of(EventType.TRANSACTION_FUNDED_INFO) == Audience.PLATFORM
    assert REGISTRY.severity_of(EventType.TRANSACTION_FUNDED_INFO) == Severity.INFO

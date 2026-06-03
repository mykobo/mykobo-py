from mykobo_py.message_bus.models.base import EventType
from mykobo_py.notification import NOTIFICATION_EVENTS


def test_notification_events_includes_relay_lifecycle():
    assert EventType.RELAY_INITIATED in NOTIFICATION_EVENTS
    assert EventType.RELAY_COMPLETED in NOTIFICATION_EVENTS
    assert EventType.RELAY_ONBOARDED in NOTIFICATION_EVENTS


def test_notification_events_includes_relay_stuck():
    assert EventType.RELAY_STUCK_DEPOSITING in NOTIFICATION_EVENTS
    assert EventType.RELAY_STUCK_BRIDGING in NOTIFICATION_EVENTS
    assert EventType.RELAY_STUCK_FORWARDING in NOTIFICATION_EVENTS


def test_notification_events_includes_relay_failed():
    assert EventType.RELAY_FAILED in NOTIFICATION_EVENTS


def test_notification_events_includes_circle_health():
    assert EventType.CIRCLE_API_5XX_BURST in NOTIFICATION_EVENTS
    assert EventType.WEBHOOK_REPROCESSOR_BACKLOG in NOTIFICATION_EVENTS


def test_notification_events_is_frozenset():
    assert isinstance(NOTIFICATION_EVENTS, frozenset)


def test_notification_events_includes_mint_burn_variants():
    mint_burn_variants = {
        EventType.MINT_COMPLETED,
        EventType.BURN_COMPLETED,
        EventType.MINT_HELD,
        EventType.BURN_HELD,
        EventType.MINT_HELD_ALERT,
        EventType.BURN_HELD_ALERT,
        EventType.CUSTOMER_NOTIFY_FAILED,
        EventType.MINT_INFO,
        EventType.BURN_INFO,
    }
    assert mint_burn_variants.issubset(NOTIFICATION_EVENTS)


def test_notification_events_does_not_include_domain_kind():
    assert EventType.NEW_TRANSACTION not in NOTIFICATION_EVENTS
    assert EventType.TRANSACTION_STATUS_UPDATE not in NOTIFICATION_EVENTS

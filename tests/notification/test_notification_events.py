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


def test_notification_events_includes_forwarding_failed():
    assert EventType.RELAY_FORWARDING_FAILED in NOTIFICATION_EVENTS


def test_notification_events_includes_circle_health():
    assert EventType.CIRCLE_API_5XX_BURST in NOTIFICATION_EVENTS
    assert EventType.WEBHOOK_REPROCESSOR_BACKLOG in NOTIFICATION_EVENTS


def test_notification_events_is_frozenset():
    assert isinstance(NOTIFICATION_EVENTS, frozenset)

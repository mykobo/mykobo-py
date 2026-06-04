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


def test_dapp_transaction_events_in_notification_events():
    from mykobo_py.message_bus.models.base import EventType
    from mykobo_py.notification.events import NOTIFICATION_EVENTS
    for ev in (
        EventType.DEPOSIT_INITIATED, EventType.DEPOSIT_COMPLETED, EventType.DEPOSIT_FAILED,
        EventType.WITHDRAW_INITIATED, EventType.WITHDRAW_COMPLETED, EventType.WITHDRAW_FAILED,
    ):
        assert ev in NOTIFICATION_EVENTS


def test_dapp_transaction_events_in_payload_type_map():
    from mykobo_py.message_bus.models.base import EventType
    from mykobo_py.message_bus.models.message import PAYLOAD_TYPE_MAP
    from mykobo_py.message_bus.models.notification import CustomerNotificationPayload
    for ev in (
        EventType.DEPOSIT_INITIATED, EventType.DEPOSIT_COMPLETED, EventType.DEPOSIT_FAILED,
        EventType.WITHDRAW_INITIATED, EventType.WITHDRAW_COMPLETED, EventType.WITHDRAW_FAILED,
    ):
        assert PAYLOAD_TYPE_MAP[ev] is CustomerNotificationPayload

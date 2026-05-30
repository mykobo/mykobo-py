from mykobo_py.message_bus.models.base import EventType


def test_new_relay_stuck_variants_exist():
    assert EventType.RELAY_STUCK_DEPOSITING.value == "RELAY_STUCK_DEPOSITING"
    assert EventType.RELAY_STUCK_BRIDGING.value == "RELAY_STUCK_BRIDGING"
    assert EventType.RELAY_STUCK_FORWARDING.value == "RELAY_STUCK_FORWARDING"


def test_relay_forwarding_failed_exists():
    assert EventType.RELAY_FORWARDING_FAILED.value == "RELAY_FORWARDING_FAILED"


def test_circle_health_variants_exist():
    assert EventType.CIRCLE_API_5XX_BURST.value == "CIRCLE_API_5XX_BURST"
    assert EventType.WEBHOOK_REPROCESSOR_BACKLOG.value == "WEBHOOK_REPROCESSOR_BACKLOG"


def test_existing_relay_variants_unchanged():
    assert EventType.RELAY_INITIATED.value == "RELAY_INITIATED"
    assert EventType.RELAY_COMPLETED.value == "RELAY_COMPLETED"
    assert EventType.RELAY_ONBOARDED.value == "RELAY_ONBOARDED"

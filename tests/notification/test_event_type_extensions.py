from mykobo_py.message_bus.models.base import EventType


def test_new_relay_stuck_variants_exist():
    assert EventType.RELAY_STUCK_DEPOSITING.value == "RELAY_STUCK_DEPOSITING"
    assert EventType.RELAY_STUCK_BRIDGING.value == "RELAY_STUCK_BRIDGING"
    assert EventType.RELAY_STUCK_FORWARDING.value == "RELAY_STUCK_FORWARDING"


def test_relay_failed_exists():
    assert EventType.RELAY_FAILED.value == "RELAY_FAILED"


def test_circle_health_variants_exist():
    assert EventType.CIRCLE_API_5XX_BURST.value == "CIRCLE_API_5XX_BURST"
    assert EventType.WEBHOOK_REPROCESSOR_BACKLOG.value == "WEBHOOK_REPROCESSOR_BACKLOG"


def test_existing_relay_variants_unchanged():
    assert EventType.RELAY_INITIATED.value == "RELAY_INITIATED"
    assert EventType.RELAY_COMPLETED.value == "RELAY_COMPLETED"
    assert EventType.RELAY_ONBOARDED.value == "RELAY_ONBOARDED"


def test_dapp_transaction_event_types_exist():
    assert EventType.DEPOSIT_INITIATED.value == "DEPOSIT_INITIATED"
    assert EventType.DEPOSIT_COMPLETED.value == "DEPOSIT_COMPLETED"
    assert EventType.DEPOSIT_FAILED.value == "DEPOSIT_FAILED"
    assert EventType.WITHDRAW_INITIATED.value == "WITHDRAW_INITIATED"
    assert EventType.WITHDRAW_COMPLETED.value == "WITHDRAW_COMPLETED"
    assert EventType.WITHDRAW_FAILED.value == "WITHDRAW_FAILED"

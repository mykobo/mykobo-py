import pytest

from mykobo_py.notification_contract.predicates import (
    And, Equals, In, NotEquals, NotIn, Or, Predicate,
)

from mykobo_py.message_bus.models.base import EventType
from mykobo_py.notification_contract import REGISTRY


def test_equals_matches():
    p: Predicate = Equals(field="status", value="FUNDS_RECEIVED")
    assert p.matches({"status": "FUNDS_RECEIVED"}) is True
    assert p.matches({"status": "PENDING"}) is False


def test_equals_missing_field_raises():
    p: Predicate = Equals(field="status", value="FUNDS_RECEIVED")
    with pytest.raises(KeyError):
        p.matches({})


def test_not_equals_matches():
    p: Predicate = NotEquals(field="status", value="PENDING")
    assert p.matches({"status": "FUNDS_RECEIVED"}) is True
    assert p.matches({"status": "PENDING"}) is False


def test_in_matches():
    p: Predicate = In(field="status", values=("FUNDS_RECEIVED", "REFUNDED"))
    assert p.matches({"status": "FUNDS_RECEIVED"}) is True
    assert p.matches({"status": "PENDING"}) is False


def test_not_in_matches():
    p: Predicate = NotIn(field="status", values=("PENDING",))
    assert p.matches({"status": "FUNDS_RECEIVED"}) is True
    assert p.matches({"status": "PENDING"}) is False


def test_and_short_circuits_when_left_false():
    # Right side would KeyError on missing "direction" if evaluated.
    # A short-circuiting And returns False without touching it.
    p: Predicate = And(
        left=Equals(field="status", value="FUNDS_RECEIVED"),
        right=Equals(field="direction", value="INBOUND"),
    )
    assert p.matches({"status": "PENDING"}) is False


def test_and_true_when_both_true():
    p: Predicate = And(
        left=Equals(field="status", value="FUNDS_RECEIVED"),
        right=Equals(field="direction", value="INBOUND"),
    )
    assert p.matches({"status": "FUNDS_RECEIVED", "direction": "INBOUND"}) is True



def test_or_true_when_either_true():
    p: Predicate = Or(
        left=Equals(field="status", value="FUNDS_RECEIVED"),
        right=Equals(field="status", value="REFUNDED"),
    )
    assert p.matches({"status": "REFUNDED"}) is True
    assert p.matches({"status": "PENDING"}) is False


def test_transaction_status_update_failed_fires_failed_alert():
    payload = {"status": "FAILED"}
    fires = REGISTRY.notifications_for(EventType.TRANSACTION_STATUS_UPDATE, payload)
    assert fires == [EventType.TRANSACTION_FAILED_ALERT]


def test_transaction_status_update_held_fires_held_alert():
    payload = {"status": "HELD"}
    fires = REGISTRY.notifications_for(EventType.TRANSACTION_STATUS_UPDATE, payload)
    assert fires == [EventType.TRANSACTION_HELD_ALERT]


def test_transaction_status_update_other_status_fires_nothing():
    payload = {"status": "PENDING_PAYER"}
    fires = REGISTRY.notifications_for(EventType.TRANSACTION_STATUS_UPDATE, payload)
    assert fires == []


def test_funds_received_status_fires_customer_email_and_platform_info():
    fires = REGISTRY.notifications_for(
        EventType.TRANSACTION_STATUS_UPDATE, {"status": "FUNDS_RECEIVED"}
    )
    assert EventType.CUSTOMER_FUNDS_RECEIVED in fires
    assert EventType.TRANSACTION_FUNDED_INFO in fires
    assert len(fires) == 2


def test_approved_status_fires_transaction_approved_info():
    fires = REGISTRY.notifications_for(
        EventType.TRANSACTION_STATUS_UPDATE, {"status": "APPROVED"}
    )
    assert fires == [EventType.TRANSACTION_APPROVED_INFO]


def test_fulfilled_status_fires_transaction_fulfilled_info():
    fires = REGISTRY.notifications_for(
        EventType.TRANSACTION_STATUS_UPDATE, {"status": "FULFILLED"}
    )
    assert fires == [EventType.TRANSACTION_FULFILLED_INFO]


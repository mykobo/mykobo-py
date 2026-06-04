import pytest

from mykobo_py.notification_contract.predicates import (
    And, Equals, In, NotEquals, NotIn, Or, Predicate,
)


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

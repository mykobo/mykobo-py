import pytest

from mykobo_py.notification_contract.predicates import (
    And, Equals, In, NotEquals, NotIn, Or, parse_predicate, PredicateParseError,
)


def test_parses_equals():
    assert parse_predicate('status == "FUNDS_RECEIVED"') == Equals("status", "FUNDS_RECEIVED")


def test_parses_not_equals():
    assert parse_predicate('status != "PENDING"') == NotEquals("status", "PENDING")


def test_parses_integer_literal():
    assert parse_predicate("attempts == 3") == Equals("attempts", 3)


def test_parses_in():
    assert parse_predicate('status in ["A", "B"]') == In("status", ("A", "B"))


def test_parses_not_in():
    assert parse_predicate('status not in ["PENDING"]') == NotIn("status", ("PENDING",))


def test_parses_and():
    assert parse_predicate('status == "A" and direction == "INBOUND"') == And(
        Equals("status", "A"), Equals("direction", "INBOUND")
    )


def test_parses_or():
    assert parse_predicate('status == "A" or status == "B"') == Or(
        Equals("status", "A"), Equals("status", "B")
    )


def test_parses_parentheses():
    parsed = parse_predicate('(status == "A" or status == "B") and direction == "IN"')
    assert parsed == And(
        Or(Equals("status", "A"), Equals("status", "B")),
        Equals("direction", "IN"),
    )


def test_rejects_arithmetic():
    with pytest.raises(PredicateParseError, match="arithmetic"):
        parse_predicate("amount + 1 == 2")


def test_rejects_function_call():
    with pytest.raises(PredicateParseError, match="function call"):
        parse_predicate('lower(status) == "a"')


def test_rejects_attribute_access():
    with pytest.raises(PredicateParseError, match="nested field"):
        parse_predicate('payload.status == "A"')


def test_rejects_unparseable():
    with pytest.raises(PredicateParseError):
        parse_predicate("status ==")


def test_rejects_bool_literal():
    with pytest.raises(PredicateParseError, match="boolean"):
        parse_predicate("flag == True")


def test_rejects_negative_int_as_arithmetic():
    with pytest.raises(PredicateParseError, match="arithmetic"):
        parse_predicate("attempts == -1")


def test_rejects_nested_list():
    with pytest.raises(PredicateParseError):
        parse_predicate('status in [[1, 2]]')


def test_rejects_unsupported_comparator():
    with pytest.raises(PredicateParseError, match="unsupported comparator"):
        parse_predicate("attempts < 3")

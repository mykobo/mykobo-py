"""Predicate AST, matcher, and parser for the notification registry's `when:` rules."""
import ast
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Equals:
    field: str
    value: object

    def matches(self, payload: dict) -> bool:
        return payload[self.field] == self.value


@dataclass(frozen=True)
class NotEquals:
    field: str
    value: object

    def matches(self, payload: dict) -> bool:
        return payload[self.field] != self.value


@dataclass(frozen=True)
class In:
    field: str
    values: tuple

    def matches(self, payload: dict) -> bool:
        return payload[self.field] in self.values


@dataclass(frozen=True)
class NotIn:
    field: str
    values: tuple

    def matches(self, payload: dict) -> bool:
        return payload[self.field] not in self.values


@dataclass(frozen=True)
class And:
    left: "Predicate"
    right: "Predicate"

    def matches(self, payload: dict) -> bool:
        return self.left.matches(payload) and self.right.matches(payload)


@dataclass(frozen=True)
class Or:
    left: "Predicate"
    right: "Predicate"

    def matches(self, payload: dict) -> bool:
        return self.left.matches(payload) or self.right.matches(payload)


Predicate = Union[Equals, NotEquals, In, NotIn, And, Or]


class PredicateParseError(ValueError):
    """Raised when a `when:` string cannot be parsed as a registry predicate."""


def parse_predicate(source: str) -> Predicate:
    """Parse a `when:` string into a Predicate AST.

    Allowed grammar:
        expr   := or_expr
        or_expr := and_expr ('or' and_expr)*
        and_expr := comp ('and' comp)*
        comp   := IDENT ('==' | '!=' | 'in' | 'not in') literal
                | '(' expr ')'
        literal := STRING | INT | '[' literal (',' literal)* ']'
    """
    try:
        tree = ast.parse(source, mode="eval")
    except SyntaxError as exc:
        raise PredicateParseError(f"could not parse predicate: {source!r}: {exc}") from exc
    return _walk(tree.body, source)


def _walk(node: ast.AST, source: str) -> Predicate:
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            return _fold(node.values, And, source)
        if isinstance(node.op, ast.Or):
            return _fold(node.values, Or, source)
        raise PredicateParseError(f"unsupported boolean op in {source!r}")

    if isinstance(node, ast.Compare):
        return _compare(node, source)

    if isinstance(node, ast.BinOp):
        raise PredicateParseError(f"arithmetic not allowed in predicate: {source!r}")
    if isinstance(node, ast.Call):
        raise PredicateParseError(f"function call not allowed in predicate: {source!r}")
    if isinstance(node, ast.Attribute):
        raise PredicateParseError(f"nested field access not allowed in predicate: {source!r}")

    raise PredicateParseError(f"unsupported expression in predicate: {source!r}")


def _fold(values, ctor, source: str) -> Predicate:
    parsed = [_walk(v, source) for v in values]
    out = parsed[0]
    for nxt in parsed[1:]:
        out = ctor(out, nxt)
    return out


def _compare(node: ast.Compare, source: str) -> Predicate:
    if len(node.ops) != 1 or len(node.comparators) != 1:
        raise PredicateParseError(f"chained comparisons not allowed: {source!r}")
    if isinstance(node.left, ast.Attribute):
        raise PredicateParseError(f"nested field access not allowed in predicate: {source!r}")
    if isinstance(node.left, ast.BinOp):
        raise PredicateParseError(f"arithmetic not allowed in predicate: {source!r}")
    if isinstance(node.left, ast.Call):
        raise PredicateParseError(f"function call not allowed in predicate: {source!r}")
    if not isinstance(node.left, ast.Name):
        raise PredicateParseError(f"left-hand side must be a field name: {source!r}")
    field = node.left.id
    op = node.ops[0]
    rhs = _literal(node.comparators[0], source)

    if isinstance(op, ast.Eq):
        return Equals(field, rhs)
    if isinstance(op, ast.NotEq):
        return NotEquals(field, rhs)
    if isinstance(op, ast.In):
        return In(field, tuple(rhs))
    if isinstance(op, ast.NotIn):
        return NotIn(field, tuple(rhs))
    raise PredicateParseError(f"unsupported comparator in predicate: {source!r}")


def _literal(node: ast.AST, source: str):
    if isinstance(node, ast.List):
        return [_scalar_literal(elt, source) for elt in node.elts]
    return _scalar_literal(node, source)


def _scalar_literal(node: ast.AST, source: str):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            raise PredicateParseError(f"boolean literal not allowed in predicate: {source!r}")
        if isinstance(node.value, (str, int)):
            return node.value
        raise PredicateParseError(f"unsupported literal in predicate: {source!r}")
    if isinstance(node, ast.UnaryOp):
        raise PredicateParseError(f"arithmetic not allowed in predicate: {source!r}")
    raise PredicateParseError(f"unsupported literal in predicate: {source!r}")

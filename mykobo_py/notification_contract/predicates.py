"""Predicate AST for the notification registry's `when:` rules.

The parser is in `parse_predicate` (next task). This module defines the
ADT and `matches(payload)` evaluation only.
"""
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

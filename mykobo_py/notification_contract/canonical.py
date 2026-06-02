"""Stable JSON projection of a Registry used for cross-library byte equivalence."""
import json
from typing import Any

from mykobo_py.notification_contract.predicates import (
    And, Equals, In, NotEquals, NotIn, Or, Predicate,
)
from mykobo_py.notification_contract.registry import (
    DomainEntry, NotificationEntry, REGISTRY_VERSION, Registry,
)


def to_canonical_dict(reg: Registry) -> dict:
    variants: dict[str, Any] = {}
    for event in sorted(reg.entries.keys(), key=lambda e: e.value):
        entry = reg.entries[event]
        if isinstance(entry, DomainEntry):
            variants[event.value] = {
                "kind": "domain",
                "notifies": [
                    {
                        "when": _predicate_to_json(r.when) if r.when else None,
                        "fires": [v.value for v in r.fires],
                    }
                    for r in entry.notifies
                ],
                "reason": entry.reason,
            }
        else:
            assert isinstance(entry, NotificationEntry)
            variants[event.value] = {
                "kind": "notification",
                "audience": entry.audience.value,
                "severity": entry.severity.value if entry.severity else None,
            }
    return {"version": REGISTRY_VERSION, "variants": variants}


def to_canonical_json(reg: Registry) -> str:
    return json.dumps(to_canonical_dict(reg), indent=2, sort_keys=True) + "\n"


def _predicate_to_json(p: Predicate) -> dict:
    if isinstance(p, Equals):
        return {"op": "eq", "field": p.field, "value": p.value}
    if isinstance(p, NotEquals):
        return {"op": "ne", "field": p.field, "value": p.value}
    if isinstance(p, In):
        return {"op": "in", "field": p.field, "values": list(p.values)}
    if isinstance(p, NotIn):
        return {"op": "not_in", "field": p.field, "values": list(p.values)}
    if isinstance(p, And):
        return {"op": "and", "left": _predicate_to_json(p.left), "right": _predicate_to_json(p.right)}
    if isinstance(p, Or):
        return {"op": "or", "left": _predicate_to_json(p.left), "right": _predicate_to_json(p.right)}
    raise TypeError(f"unknown predicate type: {type(p).__name__}")

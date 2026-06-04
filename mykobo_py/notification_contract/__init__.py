"""Producer-intended notification registry.

Public surface:
    REGISTRY                — frozen registry singleton, loaded from registry.yaml at import time
    VariantKind             — DOMAIN | NOTIFICATION
    Audience                — CUSTOMER | PLATFORM
    Severity                — INFO | WARNING | CRITICAL
    NotificationRule        — (when: Predicate | None, fires: tuple[EventType, ...])
    DomainEntry             — (notifies: tuple[NotificationRule, ...], reason: str | None)
    NotificationEntry       — (audience: Audience, severity: Severity | None)
    Predicate / parse_predicate / PredicateParseError
    RegistryError

See docs/superpowers/specs/2026-06-01-notifications-guardrail-design.md
"""
from mykobo_py.notification_contract.predicates import (
    And, Equals, In, NotEquals, NotIn, Or, Predicate, PredicateParseError, parse_predicate,
)
from mykobo_py.notification_contract.registry import (
    Audience, DomainEntry, NotificationEntry, NotificationRule, Registry,
    RegistryError, Severity, VariantKind, REGISTRY_PATH, REGISTRY_VERSION,
)

# Loaded eagerly at module import. Failure surfaces as RegistryError before
# service boot completes — fail loud rather than running with a broken contract.
REGISTRY: Registry = Registry.load()

__all__ = [
    "REGISTRY",
    "REGISTRY_PATH",
    "REGISTRY_VERSION",
    "Audience",
    "DomainEntry",
    "NotificationEntry",
    "NotificationRule",
    "Predicate",
    "PredicateParseError",
    "Registry",
    "RegistryError",
    "Severity",
    "VariantKind",
    "parse_predicate",
    "And", "Equals", "In", "NotEquals", "NotIn", "Or",
]

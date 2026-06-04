"""Notification registry: typed model, loader, query helpers.

See docs/superpowers/specs/2026-06-01-notifications-guardrail-design.md
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, Union

import yaml

from mykobo_py.message_bus.models.base import EventType
from mykobo_py.notification_contract.predicates import (
    Predicate, PredicateParseError, parse_predicate,
)

REGISTRY_VERSION = 1
REGISTRY_PATH = Path(__file__).parent / "registry.yaml"


class RegistryError(RuntimeError):
    """Raised on any invalid notification registry state."""


class VariantKind(str, Enum):
    DOMAIN = "domain"
    NOTIFICATION = "notification"


class Audience(str, Enum):
    CUSTOMER = "customer"
    PLATFORM = "platform"


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True)
class NotificationRule:
    fires: tuple[EventType, ...]
    when: Optional[Predicate] = None


@dataclass(frozen=True)
class DomainEntry:
    notifies: tuple[NotificationRule, ...]
    reason: Optional[str] = None

    @property
    def kind(self) -> VariantKind:
        return VariantKind.DOMAIN


@dataclass(frozen=True)
class NotificationEntry:
    audience: Audience
    severity: Optional[Severity] = None

    @property
    def kind(self) -> VariantKind:
        return VariantKind.NOTIFICATION


Entry = Union[DomainEntry, NotificationEntry]


@dataclass(frozen=True)
class Registry:
    entries: dict[EventType, Entry] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "Registry":
        version = data.get("version")
        if version != REGISTRY_VERSION:
            raise RegistryError(
                f"unsupported registry version: got {version!r}, expected {REGISTRY_VERSION}"
            )
        variants_raw = data.get("variants") or {}

        # Phase 1: parse every entry into either DomainEntry or NotificationEntry.
        parsed: dict[EventType, Entry] = {}
        for name, raw in variants_raw.items():
            try:
                event = EventType(name)
            except ValueError as exc:
                raise RegistryError(
                    f"YAML key {name!r} does not resolve to an EventType variant"
                ) from exc
            parsed[event] = _parse_entry(event, raw)

        # Phase 2: every enum variant must be present.
        missing = [v.value for v in EventType if v not in parsed]
        if missing:
            raise RegistryError(
                f"EventType variants missing from registry: {sorted(missing)}"
            )

        # Phase 3: every `fires` must resolve to a notification entry.
        for event, entry in parsed.items():
            if isinstance(entry, DomainEntry):
                for rule in entry.notifies:
                    for target in rule.fires:
                        target_entry = parsed.get(target)
                        if not isinstance(target_entry, NotificationEntry):
                            raise RegistryError(
                                f"{event.value}: fires target {target.value!r} "
                                "must be a kind:notification entry"
                            )

        return cls(entries=parsed)

    @classmethod
    def load(cls, path: Path = REGISTRY_PATH) -> "Registry":
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return cls.from_dict(data)

    def is_notification(self, event: EventType) -> bool:
        entry = self.entries.get(event)
        return isinstance(entry, NotificationEntry)

    def audience_of(self, event: EventType) -> Optional[Audience]:
        entry = self.entries.get(event)
        return entry.audience if isinstance(entry, NotificationEntry) else None

    def severity_of(self, event: EventType) -> Optional[Severity]:
        entry = self.entries.get(event)
        return entry.severity if isinstance(entry, NotificationEntry) else None

    def notifications_for(self, event: EventType, payload: dict) -> list[EventType]:
        entry = self.entries.get(event)
        if not isinstance(entry, DomainEntry):
            return []
        out: list[EventType] = []
        for rule in entry.notifies:
            if rule.when is None or rule.when.matches(payload):
                out.extend(rule.fires)
        return out


def _parse_entry(event: EventType, raw: dict) -> Entry:
    kind = raw.get("kind")
    if kind == VariantKind.DOMAIN.value:
        return _parse_domain(event, raw)
    if kind == VariantKind.NOTIFICATION.value:
        return _parse_notification(event, raw)
    raise RegistryError(f"{event.value}: invalid kind {kind!r}")


def _parse_domain(event: EventType, raw: dict) -> DomainEntry:
    rules_raw = raw.get("notifies")
    if rules_raw is None:
        raise RegistryError(f"{event.value}: domain entry must declare `notifies`")
    if not isinstance(rules_raw, list):
        raise RegistryError(
            f"{event.value}: `notifies` must be a list, got {type(rules_raw).__name__}"
        )
    rules: list[NotificationRule] = []
    for idx, item in enumerate(rules_raw):
        if not isinstance(item, dict):
            raise RegistryError(
                f"{event.value}: notifies[{idx}] must be a mapping, got {type(item).__name__}"
            )
        fires_raw = item.get("fires") or []
        if not fires_raw:
            raise RegistryError(
                f"{event.value}: notifies[{idx}] must declare a non-empty `fires` list"
            )
        try:
            fires = tuple(EventType(name) for name in fires_raw)
        except ValueError as exc:
            raise RegistryError(
                f"{event.value}: notifies[{idx}] fires unknown variant: {exc}"
            ) from exc
        when = None
        if "when" in item and item["when"] is not None:
            when_val = item["when"]
            if not isinstance(when_val, str):
                raise RegistryError(
                    f"{event.value}: notifies[{idx}] `when` must be a string predicate, "
                    f"got {type(when_val).__name__}"
                )
            try:
                when = parse_predicate(when_val)
            except PredicateParseError as exc:
                raise RegistryError(
                    f"{event.value}: notifies[{idx}] predicate: {exc}"
                ) from exc
        rules.append(NotificationRule(fires=fires, when=when))
    reason = raw.get("reason")
    if not rules and not reason:
        raise RegistryError(
            f"{event.value}: empty notifies requires a non-empty `reason`"
        )
    if rules and reason:
        raise RegistryError(
            f"{event.value}: `reason` is only valid when notifies is empty"
        )
    return DomainEntry(notifies=tuple(rules), reason=reason)


def _parse_notification(event: EventType, raw: dict) -> NotificationEntry:
    audience_raw = raw.get("audience")
    if isinstance(audience_raw, list):
        raise RegistryError(
            f"{event.value}: audience must be a scalar; "
            "dual-audience uses two notification variants in `fires`"
        )
    try:
        audience = Audience(audience_raw)
    except ValueError as exc:
        raise RegistryError(f"{event.value}: invalid audience {audience_raw!r}") from exc
    severity_raw = raw.get("severity")
    severity = None
    if audience == Audience.PLATFORM:
        if severity_raw is None:
            raise RegistryError(
                f"{event.value}: platform-audience notification requires a `severity`"
            )
        try:
            severity = Severity(severity_raw)
        except ValueError as exc:
            raise RegistryError(f"{event.value}: invalid severity {severity_raw!r}") from exc
    elif severity_raw is not None:
        raise RegistryError(
            f"{event.value}: customer-audience notification must not declare `severity`"
        )
    return NotificationEntry(audience=audience, severity=severity)

"""Generate cross-language notification fixtures from MessageBusMessage.to_dict().

Run from the repo root:
    poetry run python scripts/gen_notification_fixtures.py

These fixtures are paired with the equivalent set in ../mykobo-rs and are used
to assert that both libraries agree on the wire shape.
"""
import json
from pathlib import Path

from mykobo_py.message_bus.models.base import EventType
from mykobo_py.message_bus.models.message import MessageBusMessage
from mykobo_py.message_bus.models.notification import (
    CustomerNotificationPayload,
    PlatformNotificationPayload,
    RelaySubject,
    Severity,
)

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "notification"
FIXED_CREATED_AT = "2026-05-30T12:00:00Z"
FIXED_TOKEN = "test-service-token"


def _customer_msg(event, idem, data):
    payload = CustomerNotificationPayload(
        subject=RelaySubject(
            id="abc-123", source_chain="stellar", destination_chain="solana"
        ),
        data=data,
    )
    msg = MessageBusMessage.create(
        source="circle",
        payload=payload,
        service_token=FIXED_TOKEN,
        event=event,
        idempotency_key=idem,
    )
    msg.meta_data.created_at = FIXED_CREATED_AT
    return msg


def _platform_msg(event, idem, severity, subject, data):
    payload = PlatformNotificationPayload(severity=severity, data=data, subject=subject)
    msg = MessageBusMessage.create(
        source="circle",
        payload=payload,
        service_token=FIXED_TOKEN,
        event=event,
        idempotency_key=idem,
    )
    msg.meta_data.created_at = FIXED_CREATED_AT
    return msg


def build_fixtures() -> dict[str, MessageBusMessage]:
    return {
        "customer_relay_initiated.json": _customer_msg(
            EventType.RELAY_INITIATED,
            "circle:relay_initiated:abc-123",
            {
                "email": "user@example.com",
                "first_name": "Ada",
                "amount": "100.00",
                "currency": "USDC",
            },
        ),
        "customer_relay_completed.json": _customer_msg(
            EventType.RELAY_COMPLETED,
            "circle:relay_completed:abc-123",
            {
                "email": "user@example.com",
                "first_name": "Ada",
                "amount": "100.00",
                "currency": "USDC",
            },
        ),
        "customer_relay_onboarded.json": _customer_msg(
            EventType.RELAY_ONBOARDED,
            "circle:relay_onboarded:abc-123",
            {
                "email": "user@example.com",
                "first_name": "Ada",
                "amount": "100.00",
                "currency": "USDC",
            },
        ),
        "platform_relay_stuck_depositing.json": _platform_msg(
            EventType.RELAY_STUCK_DEPOSITING,
            "circle:relay_stuck_depositing:abc-123:2026-05-30T12:00:00+00:00",
            Severity.WARNING,
            "relay:abc-123",
            {
                "relay_id": "abc-123",
                "stuck_for_minutes": 22,
                "threshold_minutes": 15,
                "source_chain": "stellar",
            },
        ),
        "platform_relay_forwarding_failed.json": _platform_msg(
            EventType.RELAY_FORWARDING_FAILED,
            "circle:relay_forwarding_failed:abc-123",
            Severity.CRITICAL,
            "relay:abc-123",
            {"relay_id": "abc-123", "attempts": 5, "last_error": "timeout"},
        ),
        "platform_circle_api_5xx_burst.json": _platform_msg(
            EventType.CIRCLE_API_5XX_BURST,
            "circle:circle_api_5xx_burst:2026-05-30T12:30:00+00:00",
            Severity.WARNING,
            "service:circle:circle_api",
            {"errors_in_window": 7, "threshold": 5, "window_minutes": 15},
        ),
        "platform_webhook_reprocessor_backlog.json": _platform_msg(
            EventType.WEBHOOK_REPROCESSOR_BACKLOG,
            "circle:webhook_reprocessor_backlog:2026-05-30T12:00:00+00:00",
            Severity.WARNING,
            "service:circle:webhook_reprocessor",
            {"queue_depth": 142, "threshold": 100, "window_minutes": 60},
        ),
    }


def write_fixtures(target_dir: Path) -> list[Path]:
    target_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for filename, msg in build_fixtures().items():
        path = target_dir / filename
        path.write_text(json.dumps(msg.to_dict(), indent=2) + "\n")
        written.append(path)
    return written


if __name__ == "__main__":
    for path in write_fixtures(FIXTURES_DIR):
        print(f"wrote {path}")

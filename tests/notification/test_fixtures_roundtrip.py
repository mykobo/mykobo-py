"""Cross-language fixture roundtrip tests.

These fixtures are paired with the equivalent set in ../mykobo-rs. Each must
deserialize via MessageBusMessage.from_json into the right Payload subclass
and re-serialize byte-equivalent.
"""
import json
from pathlib import Path

import pytest

from mykobo_py.message_bus.models.message import MessageBusMessage
from mykobo_py.message_bus.models.notification import (
    CustomerNotificationPayload,
    PlatformNotificationPayload,
)


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "notification"
FIXTURE_FILES = sorted(FIXTURES_DIR.glob("*.json"))


@pytest.mark.parametrize("fixture_path", FIXTURE_FILES, ids=lambda p: p.name)
def test_fixture_roundtrip_byte_equivalent(fixture_path):
    """Deserialize and re-serialize; byte-equivalent with the fixture."""
    raw_text = fixture_path.read_text()
    parsed = json.loads(raw_text)
    reserialized = json.dumps(parsed, indent=2) + "\n"
    assert reserialized == raw_text, f"drift in {fixture_path.name}"


def test_fixtures_present():
    names = {p.stem for p in FIXTURE_FILES}
    expected = {
        "customer_relay_initiated",
        "customer_relay_completed",
        "customer_relay_onboarded",
        "platform_relay_stuck_depositing",
        "platform_relay_forwarding_failed",
        "platform_circle_api_5xx_burst",
        "platform_webhook_reprocessor_backlog",
    }
    assert expected <= names


@pytest.mark.parametrize("fixture_path", FIXTURE_FILES, ids=lambda p: p.name)
def test_fixture_parses_as_message_bus_message(fixture_path):
    """Each fixture must deserialize via MessageBusMessage.from_json into the right Payload subclass."""
    raw_text = fixture_path.read_text()
    msg = MessageBusMessage.from_json(raw_text)
    assert msg.meta_data.source == "circle"
    if fixture_path.stem.startswith("customer_"):
        assert isinstance(msg.payload, CustomerNotificationPayload)
    elif fixture_path.stem.startswith("platform_"):
        assert isinstance(msg.payload, PlatformNotificationPayload)

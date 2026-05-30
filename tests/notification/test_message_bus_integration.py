import pytest

from mykobo_py.message_bus.models.base import EventType
from mykobo_py.message_bus.models.message import MessageBusMessage
from mykobo_py.message_bus.models.notification import (
    CustomerNotificationPayload,
    PlatformNotificationPayload,
    RelaySubject,
    Severity,
)


CUSTOMER_EVENTS = [
    EventType.RELAY_INITIATED,
    EventType.RELAY_COMPLETED,
    EventType.RELAY_ONBOARDED,
]

PLATFORM_EVENTS = [
    EventType.RELAY_STUCK_DEPOSITING,
    EventType.RELAY_STUCK_BRIDGING,
    EventType.RELAY_STUCK_FORWARDING,
    EventType.RELAY_FORWARDING_FAILED,
    EventType.CIRCLE_API_5XX_BURST,
    EventType.WEBHOOK_REPROCESSOR_BACKLOG,
]


def _customer_payload():
    return CustomerNotificationPayload(
        subject=RelaySubject(id="abc", source_chain="stellar", destination_chain="solana"),
        data={"email": "u@e.com"},
    )


def _platform_payload():
    return PlatformNotificationPayload(
        severity=Severity.WARNING,
        data={"k": "v"},
        subject="relay:abc",
    )


@pytest.mark.parametrize("event", CUSTOMER_EVENTS)
def test_message_bus_message_create_for_customer_events(event):
    msg = MessageBusMessage.create(
        source="circle",
        payload=_customer_payload(),
        service_token="tok-test",
        event=event,
        idempotency_key=f"circle:{event.value.lower()}:abc",
    )
    assert msg.meta_data.event == event
    assert msg.payload.subject.id == "abc"


@pytest.mark.parametrize("event", PLATFORM_EVENTS)
def test_message_bus_message_create_for_platform_events(event):
    msg = MessageBusMessage.create(
        source="circle",
        payload=_platform_payload(),
        service_token="tok-test",
        event=event,
        idempotency_key=f"circle:{event.value.lower()}:bk",
    )
    assert msg.meta_data.event == event
    assert msg.payload.severity == Severity.WARNING


def test_wrong_payload_type_rejected():
    with pytest.raises(ValueError):
        MessageBusMessage.create(
            source="circle",
            payload=_customer_payload(),
            service_token="tok",
            event=EventType.RELAY_STUCK_DEPOSITING,  # platform event with customer payload
            idempotency_key="circle:relay_stuck_depositing:abc:bk",
        )


def test_to_dict_round_trip_via_from_json():
    msg = MessageBusMessage.create(
        source="circle",
        payload=_customer_payload(),
        service_token="tok-test",
        event=EventType.RELAY_INITIATED,
        idempotency_key="circle:relay_initiated:abc",
    )
    d = msg.to_dict()
    # token, created_at always present
    assert "token" in d["meta_data"]
    assert "created_at" in d["meta_data"]
    # ip_address and instruction_type were None -> excluded
    assert "ip_address" not in d["meta_data"]
    assert "instruction_type" not in d["meta_data"]
    # roundtrip
    import json
    msg2 = MessageBusMessage.from_json(json.dumps(d))
    assert msg2.meta_data.event == EventType.RELAY_INITIATED
    assert isinstance(msg2.payload, CustomerNotificationPayload)
    assert msg2.payload.subject.id == "abc"

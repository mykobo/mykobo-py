"""Notification-specific types that plug into the MessageBusMessage envelope.

Severity, Subjects, and NotificationPayloads are registered against the
notification EventType variants in PAYLOAD_TYPE_MAP (message.py).
"""
from enum import Enum
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator

from mykobo_py.message_bus.models.base import Payload, validate_required_fields


class Severity(str, Enum):
    """Importance gradient for PlatformNotifications."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

    def __lt__(self, other: "Severity") -> bool:
        order = [Severity.INFO, Severity.WARNING, Severity.CRITICAL]
        return order.index(self) < order.index(other)

    def __le__(self, other: "Severity") -> bool:
        return self < other or self == other

    def __gt__(self, other: "Severity") -> bool:
        return not self <= other

    def __ge__(self, other: "Severity") -> bool:
        return not self < other


class RelaySubject(BaseModel):
    type: Literal["relay"] = "relay"
    id: str
    source_chain: str
    destination_chain: str

    @model_validator(mode='after')
    def _required(self):
        validate_required_fields(self, ['id', 'source_chain', 'destination_chain'])
        return self


class TransactionSubject(BaseModel):
    type: Literal["transaction"] = "transaction"
    reference: str

    @model_validator(mode='after')
    def _required(self):
        validate_required_fields(self, ['reference'])
        return self


class ProfileSubject(BaseModel):
    type: Literal["profile"] = "profile"
    user_id: str

    @model_validator(mode='after')
    def _required(self):
        validate_required_fields(self, ['user_id'])
        return self


CustomerSubject = Annotated[
    Union[RelaySubject, TransactionSubject, ProfileSubject],
    Field(discriminator="type"),
]


class CustomerNotificationPayload(Payload):
    """Payload for customer-directed notifications (email-by-default).

    Carries a typed subject reference and a fully-rendered template-data dict.
    The dispatcher does no out-of-band lookups.
    """
    subject: CustomerSubject
    data: dict


class PlatformNotificationPayload(Payload):
    """Payload for admin-directed notifications (Slack-by-default).

    severity grades importance; subject is free-form (e.g. "relay:abc-123",
    "service:circle:webhook_reprocessor"); data is fully rendered.
    """
    severity: Severity
    data: dict
    subject: Optional[str] = None

from typing import Optional, Union
from datetime import datetime, UTC
import uuid

from pydantic import BaseModel, model_validator

from mykobo_py.message_bus.models.base import (
    Payload,
    validate_required_fields,
    InstructionType,
    EventType
)
from mykobo_py.message_bus.models.event import NewTransactionEventPayload, TransactionStatusEventPayload, \
    ProfileEventPayload, PaymentEventPayload, KycEventPayload, PasswordResetEventPayload, \
    VerificationRequestedEventPayload, AddressOnboardedEventPayload, RelayInitiatedEventPayload, \
    RelayCompletedEventPayload, RelayOnboardedEventPayload
from mykobo_py.message_bus.models.instruction import PaymentPayload, StatusUpdatePayload, CorrectionPayload, \
    TransactionPayload, UpdateProfilePayload, MintPayload, BurnPayload

PAYLOAD_TYPE_MAP = {
    InstructionType.PAYMENT: PaymentPayload,
    InstructionType.STATUS_UPDATE: StatusUpdatePayload,
    InstructionType.CORRECTION: CorrectionPayload,
    InstructionType.TRANSACTION: TransactionPayload,
    InstructionType.UPDATE_PROFILE: UpdateProfilePayload,
    InstructionType.MINT: MintPayload,
    InstructionType.BURN: BurnPayload,
    EventType.NEW_TRANSACTION: NewTransactionEventPayload,
    EventType.TRANSACTION_STATUS_UPDATE: TransactionStatusEventPayload,
    EventType.NEW_BANK_PAYMENT: PaymentEventPayload,
    EventType.NEW_PROFILE: ProfileEventPayload,
    EventType.VERIFICATION_REQUESTED: VerificationRequestedEventPayload,
    EventType.PASSWORD_RESET_REQUESTED: PasswordResetEventPayload,
    EventType.KYC_EVENT: KycEventPayload,
    EventType.ADDRESS_ONBOARDED: AddressOnboardedEventPayload,
    EventType.RELAY_INITIATED: RelayInitiatedEventPayload,
    EventType.RELAY_COMPLETED: RelayCompletedEventPayload,
    EventType.RELAY_ONBOARDED: RelayOnboardedEventPayload
}


class MetaData(BaseModel):
    """Metadata for message bus messages"""
    source: str
    created_at: str
    token: str
    idempotency_key: str
    instruction_type: Optional[InstructionType] = None
    event: Optional[EventType] = None
    ip_address: Optional[str] = None

    @model_validator(mode='after')
    def validate_fields(self):
        """Validate that all required fields are provided"""
        # Validate required base fields
        validate_required_fields(
            self,
            ['source', 'created_at', 'token', 'idempotency_key']
        )

        # Ensure at least one of instruction_type or event is provided
        if not self.instruction_type and not self.event:
            raise ValueError("MetaData must have either instruction_type or event")

        return self

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class MessageBusMessage(BaseModel):
    """Complete message bus message structure - supports multiple payload types"""
    meta_data: MetaData
    payload: Payload

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode='after')
    def validate_payload_type(self):
        """Validate that instruction_type or event matches the payload type"""
        # Determine which type field to use
        message_type = None
        if self.meta_data.instruction_type:
            message_type = self.meta_data.instruction_type
        elif self.meta_data.event:
            message_type = self.meta_data.event
        else:
            raise ValueError("Either instruction_type or event must be provided in meta_data")

        expected_payload_type = PAYLOAD_TYPE_MAP.get(message_type)
        if not expected_payload_type:
            raise ValueError(f"Unknown message type: {message_type}")

        # If payload is a dict (from JSON deserialization), convert it to the appropriate type
        if isinstance(self.payload, dict):
            self.payload = expected_payload_type.model_validate(self.payload)

        if not isinstance(self.payload, expected_payload_type):
            if isinstance(self.payload, Payload):
                self.payload = expected_payload_type.model_validate(self.payload.model_dump())
            else:
                raise ValueError(
                    f"message type {message_type}: {message_type.value} requires "
                    f"{expected_payload_type.__name__} but got {type(self.payload).__name__}"
                )

        return self

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

    @staticmethod
    def create(
        source: str,
        payload: Payload,
        service_token: str,
        instruction_type: Optional[Union[InstructionType, str]] = None,
        event: Optional[Union[EventType, str]] = None,
        idempotency_key: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> 'MessageBusMessage':
        """
        Convenience function to create a complete MessageBusMessage.

        Args:
            source: The source system (e.g., "BANKING_SERVICE", "ANCHOR_MYKOBO", "WATCHTOWER")
            payload: The payload object (any Payload subclass)
            service_token: The JWT token from the identity module
            instruction_type: The type of instruction (InstructionType enum or string). Required if event is not provided.
            event: The type of event (EventType enum or string). Required if instruction_type is not provided.
            idempotency_key: Optional idempotency key. If not provided, a UUID will be generated
            ip_address: Optional IP address

        Returns:
            A complete MessageBusMessage instance

        Raises:
            ValueError: If neither instruction_type nor event is provided, or if both are provided
        """
        # Validate that exactly one of instruction_type or event is provided
        if instruction_type is None and event is None:
            raise ValueError("Either instruction_type or event must be provided")
        if instruction_type is not None and event is not None:
            raise ValueError("Cannot specify both instruction_type and event")

        if idempotency_key is None:
            idempotency_key = str(uuid.uuid4())

        created_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

        meta_data = MetaData(
            source=source,
            instruction_type=instruction_type,
            event=event,
            created_at=created_at,
            token=service_token,
            idempotency_key=idempotency_key,
            ip_address=ip_address
        )

        return MessageBusMessage(
            meta_data=meta_data,
            payload=payload
        )

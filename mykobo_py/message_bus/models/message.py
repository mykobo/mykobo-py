from dataclasses import dataclass
from typing import Optional, Union, List, Any
from datetime import datetime, UTC
from enum import Enum
import uuid
from dataclasses_json import dataclass_json
from mykobo_py.utils import del_none


class InstructionType(str, Enum):
    """Enum for message instruction types"""
    PAYMENT = "PAYMENT"
    STATUS_UPDATE = "STATUS_UPDATE"
    CORRECTION = "CORRECTION"
    TRANSACTION = "TRANSACTION"

class TransactionType(str, Enum):
    """Enum for transaction types"""
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


def validate_required_fields(instance: Any, required_fields: List[str], class_name: str = None):
    """
    Validate that all required fields are provided and non-empty.

    Args:
        instance: The object instance to validate
        required_fields: List of field names that are required
        class_name: Optional class name for error message (defaults to instance class name)

    Raises:
        ValueError: If any required fields are missing or empty
    """
    missing_fields = []

    for field in required_fields:
        value = getattr(instance, field)
        if value is None or (isinstance(value, str) and value.strip() == ''):
            missing_fields.append(field)

    if missing_fields:
        name = class_name or instance.__class__.__name__
        raise ValueError(f"{name} missing required fields: {', '.join(missing_fields)}")


@dataclass_json
@dataclass
class MetaData:
    """Metadata for message bus messages"""
    source: str
    instruction_type: InstructionType
    created_at: str
    token: str
    idempotency_key: str

    def __post_init__(self):
        """Validate that all required fields are provided"""
        # Convert string to enum if needed
        if isinstance(self.instruction_type, str):
            self.instruction_type = InstructionType(self.instruction_type)

        validate_required_fields(
            self,
            ['source', 'instruction_type', 'created_at', 'token', 'idempotency_key']
        )

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class PaymentPayload:
    """Payload for payment instructions"""
    external_reference: str
    payer_name: Optional[str]
    currency: str
    value: str
    source: str
    reference: str
    bank_account_number: Optional[str]

    def __post_init__(self):
        """Validate that all required fields are provided"""
        validate_required_fields(
            self,
            ['external_reference', 'currency', 'value', 'source', 'reference']
        )

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class StatusUpdatePayload:
    """Payload for status update instructions"""
    reference: str
    status: str
    message: str

    def __post_init__(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['reference', 'status', 'message'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class CorrectionPayload:
    """Payload for correction instructions"""
    reference: str
    value: str
    message: str
    currency: str
    source: str

    def __post_init__(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['reference', 'value', 'message', 'currency', 'source'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class TransactionPayload:
    """Payload for transaction instructions"""
    external_reference: str
    source: str
    reference: str
    first_name: str
    last_name: str
    transaction_type: TransactionType
    status: str
    incoming_currency: str
    outgoing_currency: str
    value: str
    fee: str
    payer: Optional[str]
    payee: Optional[str]

    def __post_init__(self):
        """Validate that all required fields are provided"""
        # Convert string to enum if needed
        if isinstance(self.transaction_type, str):
            self.transaction_type = TransactionType(self.transaction_type)

        if self.transaction_type == TransactionType.DEPOSIT and self.payer is None:
            raise ValueError("Deposit transactions must be specify a payer id")

        if self.transaction_type == TransactionType.WITHDRAW and self.payee is None:
            raise ValueError("Withdraw transactions must be specify a payee id")

        validate_required_fields(
            self,
            [
                'external_reference', 'source', 'reference', 'first_name', 'last_name',
                'transaction_type', 'status', 'incoming_currency', 'outgoing_currency',
                'value', 'fee'
            ]
        )

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class MessageBusMessage:
    """Complete message bus message structure - supports multiple payload types"""
    meta_data: MetaData
    payload: Union[PaymentPayload, StatusUpdatePayload, CorrectionPayload, TransactionPayload]

    def __post_init__(self):
        """Validate that instruction_type matches the payload type"""
        # Ensure instruction_type is an enum
        if isinstance(self.meta_data.instruction_type, str):
            self.meta_data.instruction_type = InstructionType(self.meta_data.instruction_type)

        # Validate instruction_type matches payload type
        payload_type_map = {
            InstructionType.PAYMENT: PaymentPayload,
            InstructionType.STATUS_UPDATE: StatusUpdatePayload,
            InstructionType.CORRECTION: CorrectionPayload,
            InstructionType.TRANSACTION: TransactionPayload,
        }

        expected_payload_type = payload_type_map[self.meta_data.instruction_type]
        if not isinstance(self.payload, expected_payload_type):
            raise ValueError(
                f"instruction_type {self.meta_data.instruction_type.value} requires "
                f"{expected_payload_type.__name__} but got {type(self.payload).__name__}"
            )

    @property
    def to_dict(self):
        return del_none(self.to_dict())

    @staticmethod
    def create(
        source: str,
        instruction_type: Union[InstructionType, str],
        payload: Union[PaymentPayload, StatusUpdatePayload, CorrectionPayload],
        service_token: str,
        idempotency_key: Optional[str] = None
    ) -> 'MessageBusMessage':
        """
        Convenience function to create a complete MessageBusMessage.

        Args:
            source: The source system (e.g., "BANKING_SERVICE", "ANCHOR_MYKOBO", "WATCHTOWER")
            instruction_type: The type of instruction (InstructionType enum or string: "PAYMENT", "STATUS_UPDATE", "CORRECTION")
            payload: The payload object (PaymentPayload, StatusUpdatePayload, or CorrectionPayload)
            service_token: The JWT token from the identity module
            idempotency_key: Optional idempotency key. If not provided, a UUID will be generated

        Returns:
            A complete MessageBusMessage instance
        """
        if idempotency_key is None:
            idempotency_key = str(uuid.uuid4())

        created_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Convert string to enum if needed
        if isinstance(instruction_type, str):
            instruction_type = InstructionType(instruction_type)

        meta_data = MetaData(
            source=source,
            instruction_type=instruction_type,
            created_at=created_at,
            token=service_token,
            idempotency_key=idempotency_key
        )

        return MessageBusMessage(
            meta_data=meta_data,
            payload=payload
        )

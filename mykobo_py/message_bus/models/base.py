from typing import List, Any
from enum import Enum


class Payload:
    @property
    def to_dict(self):
        raise NotImplemented()


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


class InstructionType(str, Enum):
    """Enum for message instruction types"""
    PAYMENT = "PAYMENT"
    STATUS_UPDATE = "STATUS_UPDATE"
    CORRECTION = "CORRECTION"
    TRANSACTION = "TRANSACTION"
    UPDATE_PROFILE = "UPDATE_PROFILE"


class TransactionType(str, Enum):
    """Enum for transaction types"""
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Direction(str, Enum):
    """Enum for payment direction"""
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"


class EventType(str, Enum):
    """Enum for event types"""
    NEW_TRANSACTION = "NEW_TRANSACTION"
    TRANSACTION_STATUS_UPDATE = "TRANSACTION_STATUS_UPDATE"
    NEW_BANK_PAYMENT = "NEW_BANK_PAYMENT"
    NEW_CHAIN_PAYMENT = "NEW_CHAIN_PAYMENT"
    NEW_PROFILE = "NEW_PROFILE"
    NEW_USER = "NEW_USER"
    VERIFICATION_REQUESTED = "VERIFICATION_REQUESTED"
    PASSWORD_RESET_REQUESTED = "PASSWORD_RESET_REQUESTED"
    KYC_EVENT = "KYC_EVENT"

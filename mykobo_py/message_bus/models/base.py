from typing import List, Any
from enum import Enum

from pydantic import BaseModel


class Payload(BaseModel):
    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


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
    MINT = "MINT"
    BURN = "BURN"


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
    PAYMENT = "PAYMENT"
    BANK_PAYMENT = "BANK_PAYMENT"
    NEW_PROFILE = "NEW_PROFILE"
    NEW_USER = "NEW_USER"
    VERIFICATION_REQUESTED = "VERIFICATION_REQUESTED"
    PASSWORD_RESET_REQUESTED = "PASSWORD_RESET_REQUESTED"
    KYC_EVENT = "KYC_EVENT"
    ADDRESS_ONBOARDED = "ADDRESS_ONBOARDED"
    RELAY_INITIATED = "RELAY_INITIATED"
    RELAY_COMPLETED = "RELAY_COMPLETED"
    RELAY_ONBOARDED = "RELAY_ONBOARDED"
    RELAY_STUCK_DEPOSITING = "RELAY_STUCK_DEPOSITING"
    RELAY_STUCK_BRIDGING = "RELAY_STUCK_BRIDGING"
    RELAY_STUCK_FORWARDING = "RELAY_STUCK_FORWARDING"
    RELAY_FAILED = "RELAY_FAILED"
    CIRCLE_API_5XX_BURST = "CIRCLE_API_5XX_BURST"
    WEBHOOK_REPROCESSOR_BACKLOG = "WEBHOOK_REPROCESSOR_BACKLOG"
    DEPOSIT_INITIATED = "DEPOSIT_INITIATED"
    DEPOSIT_COMPLETED = "DEPOSIT_COMPLETED"
    DEPOSIT_FAILED = "DEPOSIT_FAILED"
    WITHDRAW_INITIATED = "WITHDRAW_INITIATED"
    WITHDRAW_COMPLETED = "WITHDRAW_COMPLETED"
    WITHDRAW_FAILED = "WITHDRAW_FAILED"
    MINT_COMPLETED = "MINT_COMPLETED"
    BURN_COMPLETED = "BURN_COMPLETED"
    MINT_HELD = "MINT_HELD"
    BURN_HELD = "BURN_HELD"
    MINT_HELD_ALERT = "MINT_HELD_ALERT"
    BURN_HELD_ALERT = "BURN_HELD_ALERT"
    CUSTOMER_NOTIFY_FAILED = "CUSTOMER_NOTIFY_FAILED"
    MINT_INFO = "MINT_INFO"
    BURN_INFO = "BURN_INFO"

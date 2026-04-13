from typing import Dict, Optional

from pydantic import model_validator

from mykobo_py.message_bus.models.base import TransactionType, validate_required_fields, Payload


class NewTransactionEventPayload(Payload):
    """Payload for new transaction event"""
    created_at: str
    kind: TransactionType
    reference: str
    source: str

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['created_at', 'kind', 'reference', 'source'])
        return self


class TransactionStatusEventPayload(Payload):
    """Payload for new transaction status update event"""
    reference: str
    status: str

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['reference', 'status'])
        return self


class PaymentEventPayload(Payload):
    """Payload for bank payment event"""
    external_reference: str
    reference: Optional[str] = None
    source: str

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['external_reference', 'source'])
        return self


class ProfileEventPayload(Payload):
    """Payload for new profile event"""
    title: str
    identifier: str

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['title', 'identifier'])
        return self


class KycEventPayload(Payload):
    """Payload for kyc event"""
    title: str
    identifier: str
    review_status: Optional[str] = None
    review_result: Optional[str] = None

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['title', 'identifier'])
        if self.review_status and self.review_status.lower() == 'completed':
            if not self.review_result:
                raise ValueError('review_result must be provided if review_status is completed')
        return self


class PasswordResetEventPayload(Payload):
    to: str
    subject: str
    password: str

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['to', 'subject', 'password'])
        return self


class VerificationRequestedEventPayload(Payload):
    to: str
    subject: str

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['to', 'subject'])
        return self


class AddressOnboardedEventPayload(Payload):
    email: str
    payload: Dict[str, str]

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['email'])
        return self


class RelayInitiatedEventPayload(Payload):
    email: str
    payload: Dict[str, str]

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['email'])
        return self


class RelayCompletedEventPayload(Payload):
    email: str
    payload: Dict[str, str]

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['email'])
        return self


class RelayOnboardedEventPayload(Payload):
    email: str
    payload: Dict[str, str]

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['email'])
        return self

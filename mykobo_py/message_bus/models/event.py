from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json
from mykobo_py.message_bus.models.base import TransactionType, validate_required_fields, Payload
from mykobo_py.utils import del_none


@dataclass_json
@dataclass
class NewTransactionEventPayload(Payload):
    """Payload for new transaction event"""
    created_at: str
    kind: TransactionType
    reference: str
    source: str

    def __post_init__(self):
        validate_required_fields(self, ['created_at', 'kind', 'reference', 'source'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class TransactionStatusEventPayload(Payload):
    """Payload for new transaction status update event"""
    reference: str
    status: str

    def __post_init__(self):
        validate_required_fields(self, ['reference', 'status'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class PaymentEventPayload(Payload):
    """Payload for bank payment event"""
    external_reference: str
    reference: Optional[str]
    source: str

    def __post_init__(self):
        validate_required_fields(self, ['external_reference', 'source'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class ProfileEventPayload(Payload):
    """Payload for new profile event"""
    title: str
    identifier: str

    def __post_init__(self):
        validate_required_fields(self, ['title', 'identifier'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class KycEventPayload(Payload):
    """Payload for kyc event"""
    title: str
    identifier: str
    review_status: Optional[str]
    review_result: Optional[str]

    def __post_init__(self):
        validate_required_fields(self, ['title', 'identifier'])
        if self.review_status and self.review_status.lower() == 'completed':
            if not self.review_result:
                raise ValueError('review_result must be provided if review_status is completed')

    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class PasswordResetEventPayload(Payload):
    to: str
    subject: str

    def __post_init__(self):
        validate_required_fields(self, ['to', 'subject'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class VerificationRequestedEventPayload(Payload):
    to: str
    subject: str

    def __post_init__(self):
        validate_required_fields(self, ['to', 'subject'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())

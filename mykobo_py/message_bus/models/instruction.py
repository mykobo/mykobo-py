from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from mykobo_py.message_bus.models.base import validate_required_fields, TransactionType, Direction, Payload
from mykobo_py.utils import del_none


@dataclass_json
@dataclass
class PaymentPayload(Payload):
    """Payload for payment instructions"""
    external_reference: str
    payer_name: Optional[str]
    currency: str
    value: str
    source: str
    reference: str
    direction: Direction
    bank_account_number: Optional[str]

    def __post_init__(self):
        """Validate that all required fields are provided"""
        # Convert string to enum if needed
        if isinstance(self.direction, str):
            self.direction = Direction(self.direction)

        validate_required_fields(
            self,
            ['external_reference', 'currency', 'value', 'source', 'reference', 'direction']
        )

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class StatusUpdatePayload(Payload):
    """Payload for status update instructions"""
    reference: str
    status: str
    message: Optional[str] = None

    def __post_init__(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['reference', 'status'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class CorrectionPayload(Payload):
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
class TransactionPayload(Payload):
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
class UpdateProfilePayload(Payload):
    """Payload for update profile instructions"""
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_number: Optional[str] = None
    tax_id: Optional[str] = None
    tax_id_name: Optional[str] = None
    id_country_code: Optional[str] = None
    suspended_at: Optional[str] = None
    deleted_at: Optional[str] = None

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class MintPayload(Payload):
    """Payload for mint instructions"""
    value: str
    currency: str
    reference: str
    message: Optional[str] = None

    def __post_init__(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['value', 'currency', 'reference'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class BurnPayload(Payload):
    """Payload for burn instructions"""
    value: str
    currency: str
    reference: str
    message: Optional[str] = None

    def __post_init__(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['value', 'currency', 'reference'])

    @property
    def to_dict(self):
        return del_none(self.to_dict())

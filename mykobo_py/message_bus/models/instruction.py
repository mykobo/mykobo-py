from typing import Optional

from pydantic import model_validator

from mykobo_py.message_bus.models.base import validate_required_fields, TransactionType, Direction, Payload


class PaymentPayload(Payload):
    """Payload for payment instructions"""
    external_reference: str
    payer_name: Optional[str] = None
    currency: str
    value: str
    source: str
    reference: str
    direction: Direction
    bank_account_number: Optional[str] = None

    @model_validator(mode='after')
    def validate_fields(self):
        """Validate that all required fields are provided"""
        validate_required_fields(
            self,
            ['external_reference', 'currency', 'value', 'source', 'reference', 'direction']
        )
        return self


class StatusUpdatePayload(Payload):
    """Payload for status update instructions"""
    reference: str
    status: str
    message: Optional[str] = None

    @model_validator(mode='after')
    def validate_fields(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['reference', 'status'])
        return self


class CorrectionPayload(Payload):
    """Payload for correction instructions"""
    reference: str
    value: str
    message: str
    currency: str
    source: str

    @model_validator(mode='after')
    def validate_fields(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['reference', 'value', 'message', 'currency', 'source'])
        return self


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
    payer: Optional[str] = None
    payee: Optional[str] = None

    @model_validator(mode='after')
    def validate_fields(self):
        """Validate that all required fields are provided"""
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
        return self


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


class MintPayload(Payload):
    """Payload for mint instructions"""
    value: str
    currency: str
    reference: str
    chain: str
    message: Optional[str] = None

    @model_validator(mode='after')
    def validate_fields(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['value', 'currency', 'reference', 'chain'])
        return self


class BurnPayload(Payload):
    """Payload for burn instructions"""
    value: str
    currency: str
    reference: str
    chain: str
    message: Optional[str] = None

    @model_validator(mode='after')
    def validate_fields(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['value', 'currency', 'reference', 'chain'])
        return self

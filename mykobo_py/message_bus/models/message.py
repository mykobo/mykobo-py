from dataclasses import dataclass
from typing import Optional, Union, List, Any
from dataclasses_json import dataclass_json
from mykobo_py.utils import del_none


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
    instruction_type: str
    created_at: str
    token: str

    def __post_init__(self):
        """Validate that all required fields are provided"""
        validate_required_fields(self, ['source', 'instruction_type', 'created_at', 'token'])

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
class MessageBusMessage:
    """Complete message bus message structure - supports multiple payload types"""
    meta_data: MetaData
    payload: Union[PaymentPayload, StatusUpdatePayload, CorrectionPayload]

    @property
    def to_dict(self):
        return del_none(self.to_dict())

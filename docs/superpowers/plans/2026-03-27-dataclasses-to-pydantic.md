# Dataclasses to Pydantic Migration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all dataclasses/dataclasses-json usage with pydantic BaseModel across the mykobo-py shared library while maintaining strict serialization compatibility.

**Architecture:** Bottom-up migration — start with dependencies (pyproject.toml), then base types, then leaf models, then composite models, then call sites, then tests. Each task is independently testable.

**Tech Stack:** pydantic v2, pytest

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `pyproject.toml` | Modify | Swap dataclasses-json → pydantic |
| `mykobo_py/utils.py` | Modify | Remove `del_none`, keep `LEDGER_DATE_TIME_FORMAT` |
| `mykobo_py/message_bus/models/base.py` | Modify | Replace `Payload` class with pydantic BaseModel |
| `mykobo_py/message_bus/models/instruction.py` | Modify | Convert 7 payload classes to pydantic |
| `mykobo_py/message_bus/models/event.py` | Modify | Convert 11 event payload classes to pydantic |
| `mykobo_py/message_bus/models/message.py` | Modify | Convert MetaData + MessageBusMessage to pydantic |
| `mykobo_py/identity/models/request.py` | Modify | Convert 6 request classes to pydantic |
| `mykobo_py/identity/models/response.py` | Modify | Convert 9 response classes to pydantic |
| `mykobo_py/identity/models/auth.py` | Modify | Convert Token + OtcChallenge to pydantic |
| `mykobo_py/identity/identity.py` | Modify | Update call sites (from_json → model_validate, del_none → model_dump) |
| `mykobo_py/business/models.py` | Modify | Convert FeeConfiguration to pydantic |
| `mykobo_py/business/business.py` | Modify | Update call site (to_json → model_dump_json) |
| `mykobo_py/ledger/models/request.py` | Modify | Convert 4 request classes to pydantic |
| `mykobo_py/anchor/stellar/models.py` | Modify | Convert 7 classes to pydantic |
| `mykobo_py/anchor/dapp/models.py` | Modify | Convert Transaction to pydantic |
| `mykobo_py/circle/models/request.py` | Modify | Convert 2 classes to pydantic |
| `mykobo_py/circle/circle.py` | Modify | Update call site |
| `mykobo_py/wallets/models/request.py` | Modify | Convert RegisterWalletRequest to pydantic |
| `mykobo_py/wallets/wallets.py` | Modify | Update call site |
| `mykobo_py/idenfy/models/requests.py` | Modify | Convert 2 classes to pydantic with aliases |
| `mykobo_py/idenfy/models/responses.py` | Modify | Convert 2 response classes to pydantic with aliases |
| `mykobo_py/idenfy/idenfy.py` | Modify | Update call site |
| `mykobo_py/sumsub/__init__.py` | Modify | Convert 5 classes to pydantic with aliases |
| `mykobo_py/sumsub/models/requests.py` | Modify | Convert 5 classes to pydantic with aliases |
| `mykobo_py/sumsub/sumsub.py` | Modify | Update call site |
| `mykobo_py/message_bus/kafka/kafka.py` | Modify | Update serialization call |
| `mykobo_py/message_bus/sqs/SQS.py` | Modify | Update serialization call |
| `tests/message_bus/test_message_models.py` | Modify | Update from_json → model_validate_json |
| `tests/identity/test_identity_deserialization.py` | Modify | Update from_json → model_validate |
| `tests/anchor/test_dapp_models.py` | Modify | Update from_json → model_validate, dict → model_dump |

---

### Task 1: Update dependencies

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Swap dataclasses-json for pydantic in pyproject.toml**

```python
# In pyproject.toml, replace:
dataclasses-json = "^0.6.7"
# With:
pydantic = "^2.0"
```

- [ ] **Step 2: Install new dependencies**

Run: `cd /Users/kwabena/Development/MYKOBO/mykobo-py && poetry lock && poetry install`
Expected: Successful install with pydantic added and dataclasses-json removed

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml poetry.lock
git commit -m "build: swap dataclasses-json for pydantic"
```

---

### Task 2: Convert message bus base types

**Files:**
- Modify: `mykobo_py/message_bus/models/base.py`
- Modify: `mykobo_py/utils.py`

- [ ] **Step 1: Update base.py — replace Payload class with pydantic BaseModel**

Replace the entire file content with:

```python
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
    NEW_BANK_PAYMENT = "NEW_BANK_PAYMENT"
    NEW_PROFILE = "NEW_PROFILE"
    NEW_USER = "NEW_USER"
    VERIFICATION_REQUESTED = "VERIFICATION_REQUESTED"
    PASSWORD_RESET_REQUESTED = "PASSWORD_RESET_REQUESTED"
    KYC_EVENT = "KYC_EVENT"
    ADDRESS_ONBOARDED = "ADDRESS_ONBOARDED"
    RELAY_INITIATED = "RELAY_INITIATED"
    RELAY_COMPLETED = "RELAY_COMPLETED"
    RELAY_ONBOARDED = "RELAY_ONBOARDED"
```

- [ ] **Step 2: Remove del_none from utils.py**

Replace utils.py content with:

```python
LEDGER_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
```

- [ ] **Step 3: Commit**

```bash
git add mykobo_py/message_bus/models/base.py mykobo_py/utils.py
git commit -m "refactor: convert Payload to pydantic BaseModel, remove del_none"
```

---

### Task 3: Convert instruction payloads

**Files:**
- Modify: `mykobo_py/message_bus/models/instruction.py`

- [ ] **Step 1: Replace instruction.py with pydantic models**

Replace the entire file content with:

```python
from typing import Optional

from pydantic import model_validator

from mykobo_py.message_bus.models.base import validate_required_fields, TransactionType, Direction, Payload


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

    @model_validator(mode='after')
    def validate_fields(self):
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
    payer: Optional[str]
    payee: Optional[str]

    @model_validator(mode='after')
    def validate_fields(self):
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
        validate_required_fields(self, ['value', 'currency', 'reference', 'chain'])
        return self
```

- [ ] **Step 2: Commit**

```bash
git add mykobo_py/message_bus/models/instruction.py
git commit -m "refactor: convert instruction payloads to pydantic"
```

---

### Task 4: Convert event payloads

**Files:**
- Modify: `mykobo_py/message_bus/models/event.py`

- [ ] **Step 1: Replace event.py with pydantic models**

Replace the entire file content with:

```python
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
    reference: Optional[str]
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
    review_status: Optional[str]
    review_result: Optional[str]

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['title', 'identifier'])
        if self.review_status and self.review_status.lower() == 'completed':
            if not self.review_result:
                raise ValueError('review_result must be provided if review_status is completed')
        return self


class PasswordResetEventPayload(Payload):
    """Payload for password reset event"""
    to: str
    subject: str

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['to', 'subject'])
        return self


class VerificationRequestedEventPayload(Payload):
    """Payload for verification requested event"""
    to: str
    subject: str

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['to', 'subject'])
        return self


class AddressOnboardedEventPayload(Payload):
    """Payload for address onboarded event"""
    email: str
    payload: Dict[str, str]

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['email'])
        return self


class RelayInitiatedEventPayload(Payload):
    """Payload for relay initiated event"""
    email: str
    payload: Dict[str, str]

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['email'])
        return self


class RelayCompletedEventPayload(Payload):
    """Payload for relay completed event"""
    email: str
    payload: Dict[str, str]

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['email'])
        return self


class RelayOnboardedEventPayload(Payload):
    """Payload for relay onboarded event"""
    email: str
    payload: Dict[str, str]

    @model_validator(mode='after')
    def validate_fields(self):
        validate_required_fields(self, ['email'])
        return self
```

- [ ] **Step 2: Commit**

```bash
git add mykobo_py/message_bus/models/event.py
git commit -m "refactor: convert event payloads to pydantic"
```

---

### Task 5: Convert MetaData and MessageBusMessage

**Files:**
- Modify: `mykobo_py/message_bus/models/message.py`

- [ ] **Step 1: Replace message.py with pydantic models**

Replace the entire file content with:

```python
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
    EventType.RELAY_ONBOARDED: RelayOnboardedEventPayload,
}


class MessageBusMessage(BaseModel):
    """Complete message bus message structure - supports multiple payload types"""
    meta_data: MetaData
    payload: Payload

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
        elif isinstance(self.payload, Payload) and not isinstance(self.payload, expected_payload_type):
            # payload came in as a generic Payload from JSON — try to re-validate
            self.payload = expected_payload_type.model_validate(self.payload.model_dump())

        if not isinstance(self.payload, expected_payload_type):
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

        # Convert string to enum if needed
        if instruction_type is not None and isinstance(instruction_type, str):
            instruction_type = InstructionType(instruction_type)
        if event is not None and isinstance(event, str):
            event = EventType(event)

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
```

- [ ] **Step 2: Run message bus tests**

Run: `cd /Users/kwabena/Development/MYKOBO/mykobo-py && poetry run pytest tests/message_bus/ -v`
Expected: Tests will fail because test file still uses `.from_json()` — this is expected at this stage.

- [ ] **Step 3: Commit**

```bash
git add mykobo_py/message_bus/models/message.py
git commit -m "refactor: convert MetaData and MessageBusMessage to pydantic"
```

---

### Task 6: Convert identity models

**Files:**
- Modify: `mykobo_py/identity/models/auth.py`
- Modify: `mykobo_py/identity/models/request.py`
- Modify: `mykobo_py/identity/models/response.py`

- [ ] **Step 1: Replace auth.py with pydantic models**

Replace the entire file content with:

```python
from datetime import datetime
from pydantic import BaseModel, computed_field
import jwt


class Token(BaseModel):
    subject_id: str
    token: str
    refresh_token: str | None
    expires_at: datetime

    @computed_field
    @property
    def is_expired(self) -> bool:
        return datetime.now() >= self.expires_at

    @staticmethod
    def from_json(json_data: dict) -> 'Token':
        decoded = jwt.decode(json_data["token"], options={"verify_signature": False})
        return Token(
            subject_id=json_data["subject_id"],
            token=json_data["token"],
            refresh_token=json_data["refresh_token"],
            expires_at=datetime.fromtimestamp(decoded["exp"])
        )

    @staticmethod
    def from_jwt(jwt_token: str) -> 'Token':
        decoded = jwt.decode(jwt_token, options={"verify_signature": False})
        return Token(
            subject_id=decoded["sub"],
            token=jwt_token,
            refresh_token=None,
            expires_at=datetime.fromtimestamp(decoded["exp"])
        )


class OtcChallenge(BaseModel):
    user_id: str
    otp_required: bool
    nonce: str

    @staticmethod
    def from_json(json_data: dict) -> 'OtcChallenge':
        return OtcChallenge(
            user_id=json_data["user_id"],
            otp_required=json_data["otp_required"],
            nonce=json_data["nonce"]
        )
```

Note: `Token.from_json()` and `OtcChallenge.from_json()` are kept because they contain non-trivial logic (JWT decoding) that `model_validate` cannot replicate. These are convenience constructors, not simple deserialization.

- [ ] **Step 2: Replace request.py with pydantic models**

Replace the entire file content with:

```python
from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class CustomerRequest(BaseModel):
    id: Optional[str] = None
    account: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    additional_name: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    mobile_number: Optional[str] = None
    birth_date: Optional[str] = None
    birth_country_code: Optional[str] = None
    id_country_code: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_number: Optional[str] = None
    tax_id: Optional[str] = None
    tax_id_name: Optional[str] = None
    credential_id: Optional[str] = None

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class UpdateProfileRequest(BaseModel):
    bank_account_number: Optional[str]
    bank_number: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    id_country_code: Optional[str]
    tax_id: Optional[str]
    tax_id_name: Optional[str]
    suspended_at: Optional[str]
    deleted_at: Optional[str]

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class NewDocumentRequest(BaseModel):
    profile_id: str
    document_type: str
    document_status: str
    document_path: Optional[str]
    updated_at: Optional[str]
    document_sub_type: Optional[str]
    created_at: str = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class NewKycReviewRequest(BaseModel):
    profile_id: str
    level: str

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class UserProfileFilterRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    bank_account_number: Optional[str] = None
    id_country_code: Optional[str] = None
    suspended_at: Optional[str] = None
    deleted_at: Optional[str] = None
    page: int = 1
    limit: int = 10

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class UserRiskResetRequest(BaseModel):
    comments: Optional[str] = None

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
```

- [ ] **Step 3: Replace response.py with pydantic models**

Replace the entire file content with:

```python
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class KycStatus(BaseModel):
    id: str
    profile_id: str
    review_status: str
    webhook_type: str
    applicant_id: str
    correlation_id: Optional[str]
    review_result: str
    received_at: datetime
    level_name: str
    admin_comment: Optional[str] = None
    user_comment: Optional[str] = None


class KycDocument(BaseModel):
    id: str
    profile_id: str
    document_type: str
    document_sub_type: Optional[str]
    document_status: str
    document_path: str
    reject_reason: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserProfile(BaseModel):
    id: str
    first_name: str
    last_name: str
    email_address: str
    additional_name: Optional[str]
    address: str
    mobile_number: str
    birth_date: Optional[datetime] = None
    birth_country_code: str
    bank_account_number: str
    tax_id: Optional[str] = None
    tax_id_name: Optional[str] = None
    created_at: datetime
    kyc_status: Optional[KycStatus] = None
    kyc_documents: List[KycDocument]


class ScoreIndicators(BaseModel):
    tax_residence_verified: float
    name_verified: float
    aml_passed: float
    phone_verified: float
    id_verified: float
    email_verified: float
    dob_verified: float
    residence_verified: float
    citizenship_verified: float
    is_not_pep: float


class Score(BaseModel):
    score: float
    breakdown: Dict[str, float]


class ScoreBreakdown(BaseModel):
    total_score: float
    verification: ScoreIndicators
    source_of_funds: Optional[Score] = None
    country_risk_jurisdiction: Optional[Score] = None
    expected_volume: Optional[Score] = None


class UserRiskProfile(BaseModel):
    risk_score: float
    latest_score_history: Optional[float] = None
    break_down: Optional[ScoreBreakdown] = None


class ProfileChangeLog(BaseModel):
    id: str
    profile_id: str
    changed_by_credential_id: str
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    created_at: datetime


class ProfileChangeLogResponse(BaseModel):
    profile_id: str
    total_changes: int
    logs: List[ProfileChangeLog]
```

Note: `UserRiskProfile` uses `break_down` as the field name because that is the JSON key from the API (see the existing `from_json` which reads `json_payload.get("break_down")`). Pydantic will parse this directly from the API response.

- [ ] **Step 4: Commit**

```bash
git add mykobo_py/identity/models/auth.py mykobo_py/identity/models/request.py mykobo_py/identity/models/response.py
git commit -m "refactor: convert identity models to pydantic"
```

---

### Task 7: Convert identity service client call sites

**Files:**
- Modify: `mykobo_py/identity/identity.py`

- [ ] **Step 1: Update identity.py call sites**

Replace the imports and update methods that use `del_none` / `to_dict().copy()`:

Replace the imports at the top:

```python
import json
import os
from typing import Optional

import requests
from logging import Logger
from requests import Response
from .models.auth import Token, OtcChallenge
from .models.request import CustomerRequest, NewDocumentRequest, NewKycReviewRequest, UpdateProfileRequest, \
    UserRiskResetRequest
from mykobo_py.client import MykoboServiceClient
from mykobo_py.identity.models.request import UserProfileFilterRequest
```

(Remove the `from mykobo_py.utils import del_none` import)

Then update every call site that uses `json.dumps(del_none(payload.to_dict().copy()))` to use `payload.model_dump_json(exclude_none=True)`:

- `create_new_customer`: change `data=json.dumps(del_none(payload.to_dict().copy()))` to `data=payload.model_dump_json(exclude_none=True)`
- `create_new_document`: change `data=json.dumps(del_none(payload.to_dict().copy()))` to `data=payload.model_dump_json(exclude_none=True)`
- `initiate_kyc_review`: change `data=json.dumps(del_none(payload.to_dict().copy()))` to `data=payload.model_dump_json(exclude_none=True)`
- `list_profiles`: change `data=json.dumps(del_none(filters.to_dict().copy()))` to `data=filters.model_dump_json(exclude_none=True)`
- `update_user_profile`: change `data=json.dumps(del_none(payload.to_dict().copy()))` to `data=payload.model_dump_json(exclude_none=True)`
- `reset_user_risk_score`: change `data=json.dumps(del_none(reset_request.to_dict().copy()))` to `data=reset_request.model_dump_json(exclude_none=True)`

- [ ] **Step 2: Commit**

```bash
git add mykobo_py/identity/identity.py
git commit -m "refactor: update identity client to use pydantic serialization"
```

---

### Task 8: Convert business, ledger, circle, and wallet models

**Files:**
- Modify: `mykobo_py/business/models.py`
- Modify: `mykobo_py/business/business.py`
- Modify: `mykobo_py/ledger/models/request.py`
- Modify: `mykobo_py/circle/models/request.py`
- Modify: `mykobo_py/circle/circle.py`
- Modify: `mykobo_py/wallets/models/request.py`
- Modify: `mykobo_py/wallets/wallets.py`

- [ ] **Step 1: Replace business/models.py**

```python
from pydantic import BaseModel
from typing import Optional


class FeeConfiguration(BaseModel):
    transaction_type: str
    fee_rate: float
    effective_from: str
    client_domain: str
    effective_until: Optional[str]
    created_by: str
    change_reason: str
```

- [ ] **Step 2: Update business/business.py**

Change `json=configuration.to_json()` to `json=configuration.model_dump()` in the `new_fee` method (line 37).

- [ ] **Step 3: Replace ledger/models/request.py**

```python
from pydantic import BaseModel
from typing import List, Optional


class TransactionFilterRequest(BaseModel):
    sources: List[str]
    transaction_types: List[str]
    statuses: List[str]
    currencies: List[str]
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    payee: Optional[str] = None
    payer: Optional[str] = None
    page: int
    limit: int

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class GetVerificationExceptionRequest(BaseModel):
    user_id: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    verifier_type: List[str]
    created_by: Optional[str] = None
    page: int
    limit: int

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class AddVerificationException(BaseModel):
    user_id: str
    verifier_type: str
    error_code: str
    reason: str
    created_by: str
    expires_at: Optional[str] = None

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class RevokeExceptionRequest(BaseModel):
    id: int
    revoked_by: str

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
```

- [ ] **Step 4: Replace circle/models/request.py**

```python
from pydantic import BaseModel
from typing import Optional


class RelayAddressSide(BaseModel):
    chain: str
    address: str
    private_key: str
    label: Optional[str] = None
    external_address: Optional[str] = None
    client_domain: Optional[str] = None
    email: Optional[str] = None


class CreateRelayAddressPairRequest(BaseModel):
    source: RelayAddressSide
    destination: RelayAddressSide

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
```

- [ ] **Step 5: Update circle/circle.py**

Change `data=json.dumps(request.to_dict())` to `data=request.model_dump_json(exclude_none=True)` in `create_relay_address_pair` method (line 24).

- [ ] **Step 6: Replace wallets/models/request.py**

```python
from pydantic import BaseModel


class RegisterWalletRequest(BaseModel):
    profile_id: str
    public_key: str
    memo: str | None
    chain: str

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
```

- [ ] **Step 7: Update wallets/wallets.py**

Change `data=json.dumps(request.to_dict())` to `data=request.model_dump_json(exclude_none=True)` in `register_wallet` method (line 31).

- [ ] **Step 8: Commit**

```bash
git add mykobo_py/business/models.py mykobo_py/business/business.py mykobo_py/ledger/models/request.py mykobo_py/circle/models/request.py mykobo_py/circle/circle.py mykobo_py/wallets/models/request.py mykobo_py/wallets/wallets.py
git commit -m "refactor: convert business, ledger, circle, wallet models to pydantic"
```

---

### Task 9: Convert anchor models

**Files:**
- Modify: `mykobo_py/anchor/stellar/models.py`
- Modify: `mykobo_py/anchor/dapp/models.py`

- [ ] **Step 1: Replace anchor/stellar/models.py**

```python
from pydantic import BaseModel
from typing import List


class Amount(BaseModel):
    amount: str = '0'
    asset: str = ''


class FeeDetail(BaseModel):
    name: str = ''
    description: str = ''
    amount: str = ''


class FeeDetails(BaseModel):
    total: str = '0'
    asset: str = ''
    details: List[FeeDetail] = []


class Customer(BaseModel):
    account: str = ''


class Customers(BaseModel):
    sender: Customer = Customer()
    receiver: Customer = Customer()


class Creator(BaseModel):
    account: str = ''


class Transaction(BaseModel):
    fundingMethod: str = ''
    id: str = ''
    sep: str = ''
    kind: str = ''
    status: str = ''
    type: str = ''
    amount_expected: Amount = Amount()
    amount_in: Amount = Amount()
    amount_out: Amount = Amount()
    fee_details: FeeDetails = FeeDetails()
    started_at: str = ''
    updated_at: str = ''
    message: str = ''
    destination_account: str = ''
    customers: Customers = Customers()
    creator: Creator = Creator()
    client_domain: str = ''
    client_name: str = ''
    request_client_ip_address: str = ''

    @property
    def is_pending_off_chain_funds(self):
        return self.status == "pending_user_transfer_start" and self.kind == "deposit"

    @property
    def is_pending_on_chain_fulfillment(self):
        return self.status == "pending_anchor" and self.kind == "deposit"

    @property
    def is_pending_on_chain_funds(self):
        return self.status == "pending_user_transfer_start" and self.kind == "withdrawal"

    @property
    def is_pending_off_chain_fulfillment(self):
        return self.status == "pending_anchor" and self.kind == "withdrawal"

    @property
    def has_ip_address(self):
        return self.request_client_ip_address != ""
```

Note: All fields have defaults matching the original `.get('field', '')` / `.get('field', '0')` pattern from `from_json()`. With pydantic, `Transaction.model_validate(json_data)` replaces `Transaction.from_json(json_data)`.

- [ ] **Step 2: Replace anchor/dapp/models.py**

```python
from pydantic import BaseModel
from typing import Optional


class Transaction(BaseModel):
    created_at: str = ''
    fee: str = '0'
    first_name: str = ''
    id: str = ''
    idempotency_key: str = ''
    incoming_currency: str = ''
    last_name: str = ''
    message_id: str = ''
    outgoing_currency: str = ''
    payee_id: Optional[str] = None
    payer_id: str = ''
    queue_sent_at: str = ''
    reference: str = ''
    source: str = ''
    status: str = ''
    transaction_type: str = ''
    tx_hash: Optional[str] = None
    updated_at: str = ''
    value: str = '0'
    wallet_address: str = ''
    network: Optional[str] = None
    client_domain: Optional[str] = None
    comment: Optional[str] = None

    @property
    def is_pending_anchor(self):
        return self.status == "PENDING_ANCHOR"

    @property
    def is_deposit(self):
        return self.transaction_type == "DEPOSIT"

    @property
    def is_withdrawal(self):
        return self.transaction_type == "WITHDRAWAL"

    @property
    def has_tx_hash(self):
        return self.tx_hash is not None and self.tx_hash != ""

    def dict(self, **kwargs) -> dict:
        """Backward-compatible dict method preserving None values"""
        d = self.model_dump()
        for key, value in d.items():
            if value is not None:
                d[key] = str(value)
        return d
```

Note: The `dict()` method preserves the original behavior: stringify non-None values, keep None as None. This matches the original `{k: str(v) if v is not None else None for k, v in asdict(self).items()}`.

- [ ] **Step 3: Commit**

```bash
git add mykobo_py/anchor/stellar/models.py mykobo_py/anchor/dapp/models.py
git commit -m "refactor: convert anchor models to pydantic"
```

---

### Task 10: Convert idenfy models

**Files:**
- Modify: `mykobo_py/idenfy/models/requests.py`
- Modify: `mykobo_py/idenfy/models/responses.py`

- [ ] **Step 1: Replace idenfy/models/requests.py**

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Optional


class AccessTokenRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    external_ref: str = Field(alias="externalRef")
    success_url: str = Field(alias="successUrl")
    error_url: str = Field(alias="errorUrl")
    unverified_url: str = Field(alias="unverifiedUrl")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class VerificationRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    external_ref: str = Field(alias="externalRef")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    sex: Optional[str] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    id_document_type: Optional[str] = Field(None, alias="idDocumentType")
    images: Optional[Dict[str, str]] = None
    # Session settings
    success_url: Optional[str] = Field(None, alias="successUrl")
    error_url: Optional[str] = Field(None, alias="errorUrl")
    unverified_url: Optional[str] = Field(None, alias="unverifiedUrl")
    callback_url: Optional[str] = Field(None, alias="callbackUrl")
    locale: Optional[str] = None
    expiry_time: Optional[int] = Field(None, alias="expiryTime")
    session_length: Optional[int] = Field(None, alias="sessionLength")
    token_type: Optional[str] = Field(None, alias="tokenType")
    show_instructions: Optional[bool] = Field(None, alias="showInstructions")
    generate_digit_string: Optional[bool] = Field(None, alias="generateDigitString")
    # Document data
    document_number: Optional[str] = Field(None, alias="documentNumber")
    personal_number: Optional[str] = Field(None, alias="personalNumber")
    date_of_expiry: Optional[str] = Field(None, alias="dateOfExpiry")
    date_of_issue: Optional[str] = Field(None, alias="dateOfIssue")
    # Verification features
    verify_email: Optional[bool] = Field(None, alias="verifyEmail")
    verify_phone: Optional[bool] = Field(None, alias="verifyPhone")
    verify_address: Optional[bool] = Field(None, alias="verifyAddress")
    nfc_required: Optional[bool] = Field(None, alias="nfcRequired")
    nfc_optional: Optional[bool] = Field(None, alias="nfcOptional")
    driver_license_back: Optional[bool] = Field(None, alias="driverLicenseBack")
    age_limit: Optional[int] = Field(None, alias="ageLimit")
    age_max: Optional[int] = Field(None, alias="ageMax")
    # Security checks
    check_liveness: Optional[bool] = Field(None, alias="checkLiveness")
    check_aml: Optional[bool] = Field(None, alias="checkAml")
    check_face_blacklist: Optional[bool] = Field(None, alias="checkFaceBlacklist")
    check_duplicate_faces: Optional[bool] = Field(None, alias="checkDuplicateFaces")
    check_duplicate_personal_data: Optional[bool] = Field(None, alias="checkDuplicatePersonalData")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)
```

- [ ] **Step 2: Replace idenfy/models/responses.py**

```python
from pydantic import BaseModel, Field, ConfigDict


class VerificationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auth_token: str = Field(alias="authToken")
    scan_ref: str = Field(alias="scanRef")
    client_id: str = Field(alias="clientId")


class VerificationPartialResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auth_token: str = Field(alias="authToken")
    error: str
    data_status: str = Field(alias="dataStatus")
    document_status: str = Field(alias="documentStatus")
```

- [ ] **Step 3: Commit**

```bash
git add mykobo_py/idenfy/models/requests.py mykobo_py/idenfy/models/responses.py
git commit -m "refactor: convert idenfy models to pydantic with aliases"
```

---

### Task 11: Convert sumsub models

**Files:**
- Modify: `mykobo_py/sumsub/__init__.py`
- Modify: `mykobo_py/sumsub/models/requests.py`

- [ ] **Step 1: Replace sumsub/__init__.py**

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict


class AccessTokenRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # this is our profile id. For sumsub it would be external to them.
    external_user_id: str = Field(alias="externalUserId")
    # level name is the KYC level for which to derive this token from. Usually the SEP6 level, if it's non-interactive
    level_name: str = Field(alias="levelName")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class ProfileData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class NewApplicantRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    external_user_id: str = Field(alias="externalUserId")
    level_name: str = Field(alias="levelName")
    profile: ProfileData

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class DocumentMetadata(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_doc_type: str = Field(alias="idDocType")
    id_doc_sub_type: Optional[str] = Field(None, alias="idDocSubType")
    country: Optional[str] = None

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class NewDocumentRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    metadata: DocumentMetadata
    file_path: str = Field(alias="filePath")
    applicant_id: str = Field(alias="applicantId")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)
```

- [ ] **Step 2: Replace sumsub/models/requests.py**

Same content as `sumsub/__init__.py` above (the two files currently have the same classes — `__init__.py` is the canonical version used by `sumsub/sumsub.py`). Replace with:

```python
from mykobo_py.sumsub import (
    AccessTokenRequest,
    ProfileData,
    NewApplicantRequest,
    DocumentMetadata,
    NewDocumentRequest,
)
```

This re-exports from `__init__.py` to avoid duplication.

- [ ] **Step 3: Commit**

```bash
git add mykobo_py/sumsub/__init__.py mykobo_py/sumsub/models/requests.py
git commit -m "refactor: convert sumsub models to pydantic with aliases"
```

---

### Task 12: Update Kafka and SQS call sites

**Files:**
- Modify: `mykobo_py/message_bus/kafka/kafka.py`
- Modify: `mykobo_py/message_bus/sqs/SQS.py`

- [ ] **Step 1: Update kafka.py send_message**

In the `send_message` method, change:

```python
# Before (line 98)
message_dict = json.loads(message.to_json())
# After
message_dict = message.to_dict()
```

- [ ] **Step 2: Update SQS.py send_message**

In the `send_message` method, change:

```python
# Before (line 36)
message_body = message.to_json()
# After
message_body = message.model_dump_json(exclude_none=True)
```

- [ ] **Step 3: Commit**

```bash
git add mykobo_py/message_bus/kafka/kafka.py mykobo_py/message_bus/sqs/SQS.py
git commit -m "refactor: update Kafka and SQS to use pydantic serialization"
```

---

### Task 13: Update tests — message bus

**Files:**
- Modify: `tests/message_bus/test_message_models.py`

- [ ] **Step 1: Update test deserialization calls**

In the test file, replace all instances of:
- `MetaData.from_json(json_str)` → `MetaData.model_validate_json(json_str)`
- `PaymentPayload.from_json(json_str)` → `PaymentPayload.model_validate_json(json_str)`
- `StatusUpdatePayload.from_json(json_str)` → `StatusUpdatePayload.model_validate_json(json_str)`
- `CorrectionPayload.from_json(json_str)` → `CorrectionPayload.model_validate_json(json_str)`
- `UpdateProfilePayload.from_json(json_str)` → `UpdateProfilePayload.model_validate_json(json_str)`
- `MessageBusMessage.from_json(json_str)` → `MessageBusMessage.model_validate_json(json_str)`

And replace all instances of:
- `.to_json()` → `.model_dump_json(exclude_none=True)`

Also: the test `test_metadata_valid` asserts `metadata.instruction_type == "PAYMENT"` — with pydantic, string "PAYMENT" will be auto-converted to the enum, so assert should be `metadata.instruction_type == InstructionType.PAYMENT`. Same pattern applies wherever tests pass string values and assert string equality for enum fields.

- [ ] **Step 2: Run tests**

Run: `cd /Users/kwabena/Development/MYKOBO/mykobo-py && poetry run pytest tests/message_bus/ -v`
Expected: All tests pass

- [ ] **Step 3: Commit**

```bash
git add tests/message_bus/test_message_models.py
git commit -m "test: update message bus tests for pydantic"
```

---

### Task 14: Update tests — identity deserialization

**Files:**
- Modify: `tests/identity/test_identity_deserialization.py`

- [ ] **Step 1: Update identity test call sites**

Replace:
- `UserProfile.from_json(profile.json())` → `UserProfile.model_validate(profile.json())`
- `UserProfile.from_json(response.json())` → `UserProfile.model_validate(response.json())`
- `UserRiskProfile.from_json(json_data)` → `UserRiskProfile.model_validate(json_data)`
- `ProfileChangeLogResponse.from_json(json_data)` → `ProfileChangeLogResponse.model_validate(json_data)`

Note: `UserRiskProfile` now uses `break_down` as the field name (matching the API JSON key). The test accesses `risk_profile.breakdown` — update to `risk_profile.break_down`.

- [ ] **Step 2: Run tests**

Run: `cd /Users/kwabena/Development/MYKOBO/mykobo-py && poetry run pytest tests/identity/ -v`
Expected: All tests pass

- [ ] **Step 3: Commit**

```bash
git add tests/identity/test_identity_deserialization.py
git commit -m "test: update identity tests for pydantic"
```

---

### Task 15: Update tests — dapp models

**Files:**
- Modify: `tests/anchor/test_dapp_models.py`

- [ ] **Step 1: Update dapp test call sites**

Replace all instances of:
- `Transaction.from_json(json_data)` → `Transaction.model_validate(json_data)`

The `transaction.dict()` calls stay as-is since we kept a `dict()` method on the dapp Transaction model.

- [ ] **Step 2: Run tests**

Run: `cd /Users/kwabena/Development/MYKOBO/mykobo-py && poetry run pytest tests/anchor/ -v`
Expected: All tests pass

- [ ] **Step 3: Commit**

```bash
git add tests/anchor/test_dapp_models.py
git commit -m "test: update dapp model tests for pydantic"
```

---

### Task 16: Final verification

- [ ] **Step 1: Run full test suite**

Run: `cd /Users/kwabena/Development/MYKOBO/mykobo-py && poetry run pytest -v`
Expected: All tests pass

- [ ] **Step 2: Verify no remaining dataclasses-json usage**

Run: `cd /Users/kwabena/Development/MYKOBO/mykobo-py && grep -r "dataclass_json\|dataclasses_json\|from dataclasses import\|@dataclass" mykobo_py/`
Expected: No matches (enums in base.py use `str, Enum` not `@dataclass`)

- [ ] **Step 3: Verify no remaining del_none usage**

Run: `cd /Users/kwabena/Development/MYKOBO/mykobo-py && grep -r "del_none" mykobo_py/`
Expected: No matches

- [ ] **Step 4: Commit final state if any fixups were needed**

```bash
git add -A
git commit -m "refactor: complete dataclasses to pydantic migration"
```

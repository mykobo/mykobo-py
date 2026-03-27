# Dataclasses to Pydantic Migration

**Date:** 2026-03-27
**Scope:** mykobo-py shared library — all model classes (~61 classes, 17 files, 3 test files)
**Strategy:** Big-bang migration (single pass, single version bump)

---

## Constraints

- **Strict serialization compatibility**: JSON output must be identical to current dataclasses-json output. Other services consume these messages over Kafka.
- **Major version bump**: This is a breaking API change for consumers (e.g., `from_json()` removed).

## Dependencies

- **Remove:** `dataclasses-json = "^0.6.7"`
- **Add:** `pydantic = "^2.0"`
- **Keep:** All other dependencies unchanged

---

## Model Conversion Pattern

### Standard models (currently `@dataclass_json` + `@dataclass`)

**Applies to:** message_bus models (instruction.py, event.py, message.py), identity requests, business models, ledger requests, circle requests, wallets requests

```python
# Before
@dataclass_json
@dataclass
class SomePayload:
    field: str
    optional_field: Optional[str] = None

    def __post_init__(self):
        # validation

    @property
    def to_dict(self):
        return del_none(self.to_dict())

# After
class SomePayload(BaseModel):
    field: str
    optional_field: str | None = None

    @field_validator('field')
    @classmethod
    def validate_field(cls, v):
        # validation
        return v

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
```

Key changes:
- `BaseModel` replaces both decorators
- `__post_init__` validation becomes `@field_validator` or `@model_validator`
- `to_dict()` becomes a regular method (not `@property`) calling `model_dump(exclude_none=True)`

### Aliased models (currently manual `from_json()`/`to_dict()` with camelCase mapping)

**Applies to:** identity responses, identity auth, anchor/stellar models, anchor/dapp models, idenfy models, sumsub models

```python
# Before
@dataclass
class AccessTokenRequest:
    client_id: str
    scan_ref: str

    def to_dict(self):
        return {"clientId": self.client_id, "scanRef": self.scan_ref}

    @staticmethod
    def from_json(data: dict):
        return AccessTokenRequest(client_id=data["clientId"], ...)

# After
class AccessTokenRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    client_id: str = Field(alias="clientId")
    scan_ref: str = Field(alias="scanRef")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)
```

Key changes:
- `Field(alias=...)` replaces manual camelCase mapping
- `model_validate(data)` replaces `from_json()` — pydantic resolves aliases automatically
- Nested models parsed automatically by pydantic
- Datetime fields become `datetime` type — pydantic parses ISO strings natively
- Manual `from_json()` / `from_dict()` static methods are removed

---

## Call Site Changes

### Kafka producer (`message_bus/kafka/kafka.py`)
```python
# Before
message_dict = json.loads(message.to_json())
# After
message_dict = message.to_dict()
```

### SQS (`message_bus/sqs/SQS.py`)
```python
# Before
message_body = message.to_json()
# After
message_body = message.model_dump_json(exclude_none=True)
```

### Service clients (identity, ledger, business, etc.)
```python
# Before
Token.from_json(response.json())
data = json.dumps(del_none(payload.to_dict().copy()))

# After
Token.model_validate(response.json())
data = payload.model_dump_json(exclude_none=True)
```

---

## Enums

`InstructionType`, `EventType`, `TransactionType`, `Direction` in `base.py` stay as Python `Enum`/`StrEnum`. Pydantic handles these natively — no changes needed.

---

## Removals

- `del_none()` utility from `utils.py` (replaced by `exclude_none=True`)
- All `@dataclass_json` decorators
- All `@dataclass` decorators on model classes
- All manual `from_json()` / `from_dict()` static methods
- All `__post_init__` methods (logic moves to validators)
- `dataclasses-json` from dependencies

---

## Exports

All current public exports in `__init__.py` files remain unchanged. Consumers importing `MessageBusMessage`, `PaymentPayload`, etc. still work — only the base class changes.

---

## Testing

- Update test assertions from `.from_json()` / `.to_json()` to `model_validate()` / `model_dump_json()`
- Verify JSON output against current fixtures in `tests/stubs/` for strict serialization compatibility
- Run full test suite to confirm no regressions

---

## Files to Modify

### Model files (17)
1. `mykobo_py/message_bus/models/message.py`
2. `mykobo_py/message_bus/models/instruction.py`
3. `mykobo_py/message_bus/models/event.py`
4. `mykobo_py/identity/models/response.py`
5. `mykobo_py/identity/models/request.py`
6. `mykobo_py/identity/models/auth.py`
7. `mykobo_py/business/models.py`
8. `mykobo_py/ledger/models/request.py`
9. `mykobo_py/anchor/stellar/models.py`
10. `mykobo_py/anchor/dapp/models.py`
11. `mykobo_py/circle/models/request.py`
12. `mykobo_py/wallets/models/request.py`
13. `mykobo_py/idenfy/models/requests.py`
14. `mykobo_py/idenfy/models/responses.py`
15. `mykobo_py/sumsub/__init__.py`
16. `mykobo_py/sumsub/models/requests.py`
17. `mykobo_py/utils.py` (remove `del_none`)

### Call site files
18. `mykobo_py/message_bus/kafka/kafka.py`
19. `mykobo_py/message_bus/sqs/SQS.py`
20. Service client files that call `from_json()` / `to_dict()`

### Infrastructure files
21. `pyproject.toml` (swap dependencies)
22. `mykobo_py/message_bus/__init__.py` (update exports if needed)
23. `mykobo_py/message_bus/models/__init__.py` (update exports if needed)

### Test files
24. `tests/message_bus/test_message_models.py`
25. `tests/identity/test_identity_deserialization.py`
26. `tests/anchor/test_dapp_models.py`

---

## Versioning

Major version bump (breaking change). Consuming services will need to update their dependency version and adapt call sites (`from_json()` → `model_validate()`, etc.).

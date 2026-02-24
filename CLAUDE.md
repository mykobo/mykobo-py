# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`mykobo-py` is a Python client library for interacting with the MYKOBO suite of services. It provides HTTP clients for various MYKOBO services and supports message bus communication via Kafka and AWS SQS.

**Sibling project**: `../mykobo-rs` is the Rust counterpart. Message bus models (InstructionType, EventType, payloads) must stay in sync between both libraries.

## Build and Test Commands

### Install
```bash
poetry install              # Install dependencies
```

### Testing
```bash
poetry run pytest           # Run all tests
poetry run pytest <path>    # Run specific test file
poetry run pytest -k <name> # Run tests matching name
```

### Release
```bash
make release                # Create new release (uses semantic-release)
```

## Architecture

### Core Service Clients

All service clients accept `host` and `logger` parameters and use `generate_headers()` for auth headers.

- **IdentityServiceClient** (`mykobo_py/identity/identity.py`): User authentication, profiles, KYC, authorization. Supports OTP challenges and service-to-service token acquisition.

- **WalletServiceClient** (`mykobo_py/wallets/wallets.py`): Wallet profile retrieval and registration.

- **AnchorClients** (`mykobo_py/anchor/`):
  - `stellar/anchor.py`: Stellar anchor (JSON-RPC 2.0)
  - `dapp/anchor.py`: DApp anchor (JSON-RPC 2.0)

- **BusinessServiceClient** (`mykobo_py/business/business.py`): Fee configuration and calculation.

- **LedgerServiceClient** (`mykobo_py/ledger/ledger.py`): Transaction history, compliance events, verification exceptions.

- **IdenfyServiceClient** (`mykobo_py/idenfy/idenfy.py`): Idenfy KYC integration.

- **SumsubServiceClient** (`mykobo_py/sumsub/sumsub.py`): Sumsub KYC integration.

### Message Bus Architecture

The message bus module (`mykobo_py/message_bus/`) supports Kafka and SQS:

**Kafka** (`message_bus/kafka/kafka.py`):
- `send_message(message, topic, key)` / `receive_message(topic, group_id)` / `commit_offset()`
- SASL_SSL authentication, configurable bootstrap servers

**SQS** (`message_bus/sqs/SQS.py`):
- `send_message(message, target_queue)` / `receive_message(target_queue)` / `delete_message()`
- Uses boto3, supports LocalStack endpoints

**Message Models** (`message_bus/models/`):
- `MessageBusMessage`: Core message structure with `MetaData` and `Payload`
- `InstructionType` enum: PAYMENT, STATUS_UPDATE, CORRECTION, TRANSACTION, UPDATE_PROFILE
- `EventType` enum: NEW_TRANSACTION, TRANSACTION_STATUS_UPDATE, NEW_BANK_PAYMENT, NEW_PROFILE, NEW_USER, VERIFICATION_REQUESTED, PASSWORD_RESET_REQUESTED, KYC_EVENT
- Instruction payloads: `PaymentPayload`, `StatusUpdatePayload`, `CorrectionPayload`, `TransactionPayload`, `UpdateProfilePayload`
- Event payloads: `NewTransactionEventPayload`, `TransactionStatusEventPayload`, `PaymentEventPayload`, `ProfileEventPayload`, `KycEventPayload`, `PasswordResetEventPayload`, `VerificationRequestedEventPayload`

### Model Organization

Models use `dataclasses-json` for serialization. Request/response DTOs live under each module's `models/` directory.

### Authentication Pattern

1. Service-to-service: `identity.acquire_token()` using access_key + secret_key
2. User auth: `identity.authenticate(email, password)` → may return `OtcChallenge` for OTP
3. Token refresh: `identity.refresh_token(refresh_token)`
4. Tokens have built-in expiration tracking via `Token.is_expired`

### Testing Infrastructure

- **pytest** with `requests-mock` for HTTP mocking
- Test fixtures as JSON files in `tests/stubs/`
- Test structure mirrors source layout

## Environment Variables

- Identity: `IDENTITY_SERVICE_HOST`, `IDENTITY_ACCESS_KEY`, `IDENTITY_SECRET_KEY`
- Wallets: `WALLET_SERVICE_HOST`
- Kafka: `KAFKA_BOOTSTRAP_SERVERS`
- AWS: `AWS_REGION` (defaults to `eu-west-1`)

## Key Patterns

### Error Handling
Service methods return `requests.Response` objects and call `.raise_for_status()` for HTTP errors.

### Message Bus
```python
message = MessageBusMessage.create(
    source="BANKING_SERVICE",
    instruction_type=InstructionType.PAYMENT,
    payload=PaymentPayload(...),
    service_token="jwt.token"
)
```
- `idempotency_key` auto-generates UUID if not provided
- `created_at` auto-set to current UTC time
- Exactly one of `instruction_type` or `event` must be provided

### Keeping in Sync with mykobo-rs
When modifying message bus models, ensure changes are mirrored in `../mykobo-rs/src/message_bus/models/`. Key files to keep aligned:
- `base.py` ↔ `base.rs` (enums)
- `instruction.py` ↔ `instruction.rs` (instruction payloads)
- `event.py` ↔ `event.rs` (event payloads)
- `message.py` ↔ `message.rs` (MetaData, Payload enum, MessageBusMessage)

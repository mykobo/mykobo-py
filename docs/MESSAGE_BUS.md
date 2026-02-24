# Message Bus Clients

This document describes how to use the message bus clients (SQS and Kafka) for sending and receiving messages.

## Table of Contents

- [Overview](#overview)
- [SQS Client](#sqs-client)
- [Kafka Client](#kafka-client)
- [Message Bus Messages](#message-bus-messages)

## Overview

The message bus package provides clients for interacting with both AWS SQS and Apache Kafka. Both clients support sending and receiving `MessageBusMessage` objects or plain dictionaries.

## SQS Client

### Initialization

```python
from mykobo_py.message_bus.sqs import SQS

# Initialize with queue URL
sqs = SQS(queue_url="http://localhost:4566")
```

**Configuration:**
- `queue_url`: The base URL for your SQS service (required)
- Uses `AWS_REGION` environment variable (defaults to `eu-west-1`)

### Sending Messages

```python
from mykobo_py.message_bus.models import MessageBusMessage, InstructionType, PaymentPayload, Direction

# Create a message using the convenience function
message = MessageBusMessage.create(
    source="BANKING_SERVICE",
    instruction_type=InstructionType.PAYMENT,
    payload=PaymentPayload(
        external_reference="P123",
        payer_name="John Doe",
        currency="EUR",
        value="100.00",
        source="BANK",
        reference="REF123",
        direction="INBOUND",
        bank_account_number="GB123"
    ),
    service_token="your.jwt.token",
    idempotency_key="unique-key-123"
)

# Send the message
response = sqs.send_message(message, target_queue="payment-queue")
```

**Or send a plain dictionary:**

```python
message_dict = {
    "meta_data": {
        "source": "BANKING_SERVICE",
        "instruction_type": "PAYMENT",
        "created_at": "2021-01-01T00:00:00Z",
        "token": "your.jwt.token",
        "idempotency_key": "key-123"
    },
    "payload": {
        "external_reference": "P123",
        "currency": "EUR",
        "value": "100.00",
        "source": "BANK",
        "reference": "REF123"
    }
}

response = sqs.send_message(message_dict, target_queue="payment-queue")
```

### Receiving Messages

```python
# Receive a message from a queue
result = sqs.receive_message(target_queue="payment-queue")

if result:
    receipt_handle, message_body = list(result.items())[0]

    # Process the message
    print(f"Received: {message_body}")

    # Delete the message after processing
    sqs.delete_message(target_queue="payment-queue", receipt_handle=receipt_handle)
```

## Kafka Client

### Initialization

```python
from mykobo_py.message_bus.kafka import Kafka

# Initialize with bootstrap servers (string or list)
kafka = Kafka(bootstrap_servers="localhost:9092")

# Or with multiple servers
kafka = Kafka(bootstrap_servers=["kafka1:9092", "kafka2:9092"])

# With authentication (for production environments)
kafka = Kafka(
    bootstrap_servers="kafka.example.com:9092",
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    user_name="my_user",
    password="my_password"
)

# With client IDs for producer and consumer
kafka = Kafka(
    bootstrap_servers="kafka.example.com:9092",
    producer_id="my-service-producer",
    consumer_id="my-service-consumer",
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    user_name="my_user",
    password="my_password"
)
```

**Configuration:**
- `bootstrap_servers`: Kafka broker address(es). Can be:
  - String with single broker: `"localhost:9092"`
  - String with multiple brokers (comma-separated): `"kafka1:9092,kafka2:9092"`
  - List of brokers: `["kafka1:9092", "kafka2:9092"]`
  - If not provided, uses `KAFKA_BOOTSTRAP_SERVERS` environment variable (defaults to `localhost:9092`)

**Keyword Arguments:**
- `producer_id`: Client ID for the producer (optional, for monitoring/debugging)
- `consumer_id`: Client ID for the consumer (optional, for monitoring/debugging)
- `security_protocol`: Security protocol (defaults to `SASL_SSL`)
- `sasl_mechanism`: SASL mechanism (defaults to `PLAIN`)
- `user_name`: Username for authentication (optional)
- `password`: Password for authentication (optional)

**Note:** Authentication parameters (`security_protocol`, `sasl_mechanism`, `user_name`, `password`) apply to both the producer and all consumers created by this client instance.

### Sending Messages

```python
from mykobo_py.message_bus.models import MessageBusMessage, InstructionType, PaymentPayload, Direction

# Create a message using the convenience function
message = MessageBusMessage.create(
    source="BANKING_SERVICE",
    instruction_type=InstructionType.PAYMENT,
    payload=PaymentPayload(
        external_reference="P123",
        payer_name="John Doe",
        currency="EUR",
        value="100.00",
        source="BANK",
        reference="REF123",
        direction="INBOUND",
        bank_account_number="GB123"
    ),
    service_token="your.jwt.token",
    idempotency_key="unique-key-123"
)

# Send to a topic
metadata = kafka.send_message(message, topic="transactions")
print(f"Message sent to partition {metadata.partition} at offset {metadata.offset}")

# Send with a partition key (for ordering guarantees)
metadata = kafka.send_message(
    message,
    topic="transactions",
    key="user-123"  # All messages with same key go to same partition
)
```

**Or send a plain dictionary:**

```python
message_dict = {
    "meta_data": {
        "source": "BANKING_SERVICE",
        "instruction_type": "PAYMENT",
        "created_at": "2021-01-01T00:00:00Z",
        "token": "your.jwt.token",
        "idempotency_key": "key-123"
    },
    "payload": {
        "external_reference": "P123",
        "currency": "EUR",
        "value": "100.00",
        "source": "BANK",
        "reference": "REF123"
    }
}

metadata = kafka.send_message(message_dict, topic="transactions")
```

### Receiving Messages

```python
# Receive a message from a topic
result = kafka.receive_message(
    topic="transactions",
    group_id="my-service",  # Consumer group ID
    timeout_ms=1000  # Max wait time for a message
)

if result:
    receipt_handle, message_body = list(result.items())[0]

    # Process the message
    print(f"Received: {message_body}")

    # Commit the offset after processing
    kafka.commit_offset(topic="transactions", receipt_handle=receipt_handle)
```

**Consumer Groups:**
- If `group_id` is not provided, a default group is created: `{topic}_consumer_group`
- Messages are load-balanced across consumers in the same group
- Each consumer group maintains its own offset tracking

**Advanced Options:**

```python
# Auto-commit offsets (not recommended for most cases)
result = kafka.receive_message(
    topic="transactions",
    group_id="my-service",
    auto_commit=True  # Automatically commit offsets
)

# Custom timeout
result = kafka.receive_message(
    topic="transactions",
    group_id="my-service",
    timeout_ms=5000  # Wait up to 5 seconds
)
```

### Closing Connections

```python
# Close all Kafka connections when done
kafka.close()
```

## Message Bus Messages

Both SQS and Kafka clients work with `MessageBusMessage` objects or plain dictionaries.

### Creating Messages with the Convenience Function

```python
from mykobo_py.message_bus.models import (
    MessageBusMessage,
    InstructionType,
    EventType,
    PaymentPayload,
    TransactionStatusEventPayload
)

# For instructions
payment_message = MessageBusMessage.create(
    source="BANKING_SERVICE",
    instruction_type=InstructionType.PAYMENT,
    payload=PaymentPayload(...),
    service_token="your.jwt.token"
)

# For events
status_event = MessageBusMessage.create(
    source="BANKING_SERVICE",
    event=EventType.TRANSACTION_STATUS_UPDATE,
    payload=TransactionStatusEventPayload(...),
    service_token="your.jwt.token"
)
```

### Available Instruction Types

- `InstructionType.PAYMENT`
- `InstructionType.STATUS_UPDATE`
- `InstructionType.CORRECTION`
- `InstructionType.TRANSACTION`

### Available Event Types

- `EventType.NEW_TRANSACTION`
- `EventType.TRANSACTION_STATUS_UPDATE`
- `EventType.NEW_BANK_PAYMENT`
- `EventType.NEW_PROFILE`
- `EventType.VERIFICATION_REQUESTED`
- `EventType.PASSWORD_RESET_REQUESTED`
- `EventType.KYC_EVENT`

### Message Structure

All messages follow this structure:

```python
{
    "meta_data": {
        "source": "BANKING_SERVICE",          # Source system
        "instruction_type": "PAYMENT",         # Or "event" for events
        "created_at": "2021-01-01T00:00:00Z", # ISO 8601 timestamp
        "token": "your.jwt.token",            # Service authentication token
        "idempotency_key": "unique-key"       # For duplicate detection
    },
    "payload": {
        # Payload structure depends on instruction_type/event
        # See payload classes for specific fields
    }
}
```

## Key Differences Between SQS and Kafka

| Feature | SQS | Kafka |
|---------|-----|-------|
| **Message Deletion** | `delete_message()` - removes from queue | `commit_offset()` - marks as read, message stays in topic |
| **Consumer Groups** | Not applicable | Supported via `group_id` parameter |
| **Ordering** | FIFO queues only | Guaranteed per partition (use `key` for routing) |
| **Message Retention** | Deleted after processing | Retained per topic configuration |
| **Load Balancing** | Multiple receivers can poll same queue | Automatic within consumer group |
| **Partition Key** | Not applicable | Use `key` parameter in `send_message()` |

## Example: Complete Workflow

### SQS Example

```python
from mykobo_py.message_bus.sqs import SQS
from mykobo_py.message_bus.models import MessageBusMessage, InstructionType, PaymentPayload, Direction

# Initialize
sqs = SQS(queue_url="http://localhost:4566")

# Create and send message
message = MessageBusMessage.create(
    source="BANKING_SERVICE",
    instruction_type=InstructionType.PAYMENT,
    payload=PaymentPayload(
        external_reference="P123",
        payer_name="John Doe",
        currency="EUR",
        value="100.00",
        source="BANK",
        reference="REF123",
        direction="INBOUND",
        bank_account_number="GB123"
    ),
    service_token="your.jwt.token"
)

sqs.send_message(message, target_queue="payment-queue")

# Receive and process
result = sqs.receive_message(target_queue="payment-queue")
if result:
    receipt_handle, message_body = list(result.items())[0]
    # Process message...
    sqs.delete_message(target_queue="payment-queue", receipt_handle=receipt_handle)
```

### Kafka Example

```python
from mykobo_py.message_bus.kafka import Kafka
from mykobo_py.message_bus.models import MessageBusMessage, InstructionType, PaymentPayload, Direction

# Initialize with authentication and client IDs
kafka = Kafka(
    bootstrap_servers="kafka.example.com:9092",
    producer_id="payment-service-producer",
    consumer_id="payment-service-consumer",
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    user_name="my_user",
    password="my_password"
)

# Create and send message
message = MessageBusMessage.create(
    source="BANKING_SERVICE",
    instruction_type=InstructionType.PAYMENT,
    payload=PaymentPayload(
        external_reference="P123",
        payer_name="John Doe",
        currency="EUR",
        value="100.00",
        source="BANK",
        reference="REF123",
        direction="INBOUND",
        bank_account_number="GB123"
    ),
    service_token="your.jwt.token"
)

# Send with partition key for ordering
kafka.send_message(message, topic="payments", key="user-123")

# Receive and process
result = kafka.receive_message(topic="payments", group_id="payment-processor")
if result:
    receipt_handle, message_body = list(result.items())[0]
    # Process message...
    kafka.commit_offset(topic="payments", receipt_handle=receipt_handle)

# Cleanup
kafka.close()
```

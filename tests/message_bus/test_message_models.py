import pytest
import json
from datetime import datetime
from mykobo_py.message_bus.models import (
    MessageBusMessage,
    MetaData,
    PaymentPayload,
    StatusUpdatePayload,
    CorrectionPayload,
    InstructionType,
    EventType,
)


class TestMetaData:
    """Tests for MetaData model"""

    def test_metadata_valid(self):
        """Test creating valid MetaData"""
        metadata = MetaData(
            source="BANKING_SERVICE",
            instruction_type="PAYMENT",
            created_at="2021-01-01T00:00:00Z",
            token="test.token.here",
            idempotency_key="unique-key-123"
        )
        assert metadata.source == "BANKING_SERVICE"
        assert metadata.instruction_type == "PAYMENT"
        assert metadata.created_at == "2021-01-01T00:00:00Z"
        assert metadata.token == "test.token.here"
        assert metadata.idempotency_key == "unique-key-123"

    def test_metadata_missing_source(self):
        """Test MetaData validation fails when source is missing"""
        with pytest.raises(ValueError) as exc_info:
            MetaData(
                source="",
                instruction_type="PAYMENT",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here",
                idempotency_key="unique-key-123"
            )
        assert "MetaData missing required fields: source" in str(exc_info.value)

    def test_metadata_missing_instruction_type_and_event(self):
        """Test MetaData validation fails when both instruction_type and event are missing"""
        with pytest.raises(ValueError) as exc_info:
            MetaData(
                source="BANKING_SERVICE",
                instruction_type=None,
                event=None,
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here",
                idempotency_key="unique-key-123"
            )
        assert "instruction_type or event" in str(exc_info.value)

    def test_metadata_missing_multiple_fields(self):
        """Test MetaData validation fails when multiple fields are missing"""
        with pytest.raises(ValueError) as exc_info:
            MetaData(
                source="",
                instruction_type="PAYMENT",
                created_at="",
                token="",
                idempotency_key=""
            )
        assert "source" in str(exc_info.value)
        assert "created_at" in str(exc_info.value)
        assert "token" in str(exc_info.value)
        assert "idempotency_key" in str(exc_info.value)

    def test_metadata_from_json(self):
        """Test deserializing MetaData from JSON"""
        json_str = json.dumps({
            "source": "BANKING_SERVICE",
            "instruction_type": "PAYMENT",
            "created_at": "2021-01-01T00:00:00Z",
            "token": "test.token.here",
            "idempotency_key": "unique-key-123"
        })
        metadata = MetaData.from_json(json_str)
        assert metadata.source == "BANKING_SERVICE"
        assert metadata.instruction_type == "PAYMENT"
        assert metadata.idempotency_key == "unique-key-123"

    def test_metadata_missing_idempotency_key(self):
        """Test MetaData validation fails when idempotency_key is missing"""
        with pytest.raises(ValueError) as exc_info:
            MetaData(
                source="BANKING_SERVICE",
                instruction_type="PAYMENT",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here",
                idempotency_key=""
            )
        assert "idempotency_key" in str(exc_info.value)

    def test_metadata_with_enum_instruction_type(self):
        """Test MetaData with InstructionType enum"""
        metadata = MetaData(
            source="BANKING_SERVICE",
            instruction_type=InstructionType.PAYMENT,
            created_at="2021-01-01T00:00:00Z",
            token="test.token.here",
            idempotency_key="unique-key-123"
        )
        assert metadata.instruction_type == InstructionType.PAYMENT
        assert metadata.instruction_type.value == "PAYMENT"

    def test_metadata_string_converts_to_enum(self):
        """Test MetaData converts string instruction_type to enum"""
        metadata = MetaData(
            source="BANKING_SERVICE",
            instruction_type="STATUS_UPDATE",
            created_at="2021-01-01T00:00:00Z",
            token="test.token.here",
            idempotency_key="unique-key-123"
        )
        assert metadata.instruction_type == InstructionType.STATUS_UPDATE
        assert isinstance(metadata.instruction_type, InstructionType)

    def test_metadata_invalid_instruction_type(self):
        """Test MetaData raises error for invalid instruction_type"""
        with pytest.raises(ValueError) as exc_info:
            MetaData(
                source="BANKING_SERVICE",
                instruction_type="INVALID_TYPE",
                event=None,
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here",
                idempotency_key="unique-key-123"
            )
        assert "INVALID_TYPE" in str(exc_info.value)

    def test_metadata_with_event(self):
        """Test MetaData with event field"""
        metadata = MetaData(
            source="BANKING_SERVICE",
            instruction_type=None,
            event=EventType.NEW_TRANSACTION,
            created_at="2021-01-01T00:00:00Z",
            token="test.token.here",
            idempotency_key="unique-key-123"
        )
        assert metadata.event == EventType.NEW_TRANSACTION
        assert metadata.instruction_type is None

    def test_metadata_event_string_converts_to_enum(self):
        """Test MetaData converts string event to enum"""
        metadata = MetaData(
            source="BANKING_SERVICE",
            instruction_type=None,
            event="NEW_TRANSACTION",
            created_at="2021-01-01T00:00:00Z",
            token="test.token.here",
            idempotency_key="unique-key-123"
        )
        assert metadata.event == EventType.NEW_TRANSACTION
        assert isinstance(metadata.event, EventType)


class TestPaymentPayload:
    """Tests for PaymentPayload model"""

    def test_payment_payload_valid(self):
        """Test creating valid PaymentPayload"""
        payload = PaymentPayload(
            external_reference="P763763453G",
            payer_name="John Doe",
            currency="EUR",
            value="123.00",
            source="BANK_MODULR",
            reference="MYK123344545",
            bank_account_number="GB123266734836738787454"
        )
        assert payload.external_reference == "P763763453G"
        assert payload.currency == "EUR"
        assert payload.value == "123.00"

    def test_payment_payload_optional_fields(self):
        """Test PaymentPayload with optional fields as None"""
        payload = PaymentPayload(
            external_reference="P763763453G",
            payer_name=None,
            currency="EUR",
            value="123.00",
            source="BANK_MODULR",
            reference="MYK123344545",
            bank_account_number=None
        )
        assert payload.payer_name is None
        assert payload.bank_account_number is None

    def test_payment_payload_missing_required_field(self):
        """Test PaymentPayload validation fails when required field is missing"""
        with pytest.raises(ValueError) as exc_info:
            PaymentPayload(
                external_reference="",
                payer_name="John Doe",
                currency="EUR",
                value="123.00",
                source="BANK_MODULR",
                reference="MYK123344545",
                bank_account_number="GB123266734836738787454"
            )
        assert "external_reference" in str(exc_info.value)

    def test_payment_payload_from_json(self):
        """Test deserializing PaymentPayload from JSON"""
        json_str = json.dumps({
            "external_reference": "P763763453G",
            "payer_name": "John Doe",
            "currency": "EUR",
            "value": "123.00",
            "source": "BANK_MODULR",
            "reference": "MYK123344545",
            "bank_account_number": "GB123266734836738787454"
        })
        payload = PaymentPayload.from_json(json_str)
        assert payload.external_reference == "P763763453G"
        assert payload.payer_name == "John Doe"


class TestStatusUpdatePayload:
    """Tests for StatusUpdatePayload model"""

    def test_status_update_payload_valid(self):
        """Test creating valid StatusUpdatePayload"""
        payload = StatusUpdatePayload(
            reference="MYK123344545",
            status="PENDING_SERVICE",
            message="Payment was received, waiting for stockist to provide asset"
        )
        assert payload.reference == "MYK123344545"
        assert payload.status == "PENDING_SERVICE"
        assert payload.message == "Payment was received, waiting for stockist to provide asset"

    def test_status_update_payload_missing_field(self):
        """Test StatusUpdatePayload validation fails when field is missing"""
        with pytest.raises(ValueError) as exc_info:
            StatusUpdatePayload(
                reference="MYK123344545",
                status="",
                message="Payment was received"
            )
        assert "status" in str(exc_info.value)

    def test_status_update_payload_from_json(self):
        """Test deserializing StatusUpdatePayload from JSON"""
        json_str = json.dumps({
            "reference": "MYK123344545",
            "status": "PENDING_SERVICE",
            "message": "Payment was received"
        })
        payload = StatusUpdatePayload.from_json(json_str)
        assert payload.reference == "MYK123344545"
        assert payload.status == "PENDING_SERVICE"


class TestCorrectionPayload:
    """Tests for CorrectionPayload model"""

    def test_correction_payload_valid(self):
        """Test creating valid CorrectionPayload"""
        payload = CorrectionPayload(
            reference="MYK123344545",
            value="2.00",
            message="Over paid through some different source",
            currency="EUR",
            source="BANK_WISE"
        )
        assert payload.reference == "MYK123344545"
        assert payload.value == "2.00"
        assert payload.currency == "EUR"
        assert payload.source == "BANK_WISE"

    def test_correction_payload_missing_field(self):
        """Test CorrectionPayload validation fails when field is missing"""
        with pytest.raises(ValueError) as exc_info:
            CorrectionPayload(
                reference="",
                value="2.00",
                message="Over paid",
                currency="EUR",
                source="BANK_WISE"
            )
        assert "reference" in str(exc_info.value)

    def test_correction_payload_from_json(self):
        """Test deserializing CorrectionPayload from JSON"""
        json_str = json.dumps({
            "reference": "MYK123344545",
            "value": "2.00",
            "message": "Over paid through some different source",
            "currency": "EUR",
            "source": "BANK_WISE"
        })
        payload = CorrectionPayload.from_json(json_str)
        assert payload.reference == "MYK123344545"
        assert payload.value == "2.00"


class TestMessageBusMessage:
    """Tests for MessageBusMessage model"""

    def test_payment_message_valid(self):
        """Test creating valid payment message"""
        message = MessageBusMessage(
            meta_data=MetaData(
                source="BANKING_SERVICE",
                instruction_type="PAYMENT",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here",
                idempotency_key="unique-key-123"
            ),
            payload=PaymentPayload(
                external_reference="P763763453G",
                payer_name="John Doe",
                currency="EUR",
                value="123.00",
                source="BANK_MODULR",
                reference="MYK123344545",
                bank_account_number="GB123266734836738787454"
            )
        )
        assert message.meta_data.source == "BANKING_SERVICE"
        assert message.meta_data.instruction_type == "PAYMENT"
        assert message.meta_data.idempotency_key == "unique-key-123"
        assert isinstance(message.payload, PaymentPayload)
        assert message.payload.external_reference == "P763763453G"

    def test_status_update_message_valid(self):
        """Test creating valid status update message"""
        message = MessageBusMessage(
            meta_data=MetaData(
                source="ANCHOR_MYKOBO",
                instruction_type="STATUS_UPDATE",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here",
                idempotency_key="unique-key-456"
            ),
            payload=StatusUpdatePayload(
                reference="MYK123344545",
                status="PENDING_SERVICE",
                message="Payment was received"
            )
        )
        assert message.meta_data.source == "ANCHOR_MYKOBO"
        assert message.meta_data.idempotency_key == "unique-key-456"
        assert isinstance(message.payload, StatusUpdatePayload)
        assert message.payload.status == "PENDING_SERVICE"

    def test_correction_message_valid(self):
        """Test creating valid correction message"""
        message = MessageBusMessage(
            meta_data=MetaData(
                source="WATCHTOWER",
                instruction_type="CORRECTION",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here",
                idempotency_key="unique-key-789"
            ),
            payload=CorrectionPayload(
                reference="MYK123344545",
                value="2.00",
                message="Over paid",
                currency="EUR",
                source="BANK_WISE"
            )
        )
        assert message.meta_data.source == "WATCHTOWER"
        assert message.meta_data.idempotency_key == "unique-key-789"
        assert isinstance(message.payload, CorrectionPayload)
        assert message.payload.value == "2.00"

    def test_payment_message_from_json(self):
        """Test deserializing payment message from JSON"""
        json_str = json.dumps({
            "meta_data": {
                "source": "BANKING_SERVICE",
                "instruction_type": "PAYMENT",
                "created_at": "2021-01-01T00:00:00Z",
                "token": "test.token.here",
                "idempotency_key": "unique-key-123"
            },
            "payload": {
                "external_reference": "P763763453G",
                "payer_name": "John Doe",
                "currency": "EUR",
                "value": "123.00",
                "source": "BANK_MODULR",
                "reference": "MYK123344545",
                "bank_account_number": "GB123266734836738787454"
            }
        })
        message = MessageBusMessage.from_json(json_str)
        assert message.meta_data.source == "BANKING_SERVICE"
        assert message.meta_data.idempotency_key == "unique-key-123"
        assert message.payload.external_reference == "P763763453G"

    def test_status_update_message_from_json(self):
        """Test deserializing status update message from JSON"""
        json_str = json.dumps({
            "meta_data": {
                "source": "ANCHOR_MYKOBO",
                "instruction_type": "STATUS_UPDATE",
                "created_at": "2021-01-01T00:00:00Z",
                "token": "test.token.here",
                "idempotency_key": "unique-key-456"
            },
            "payload": {
                "reference": "MYK123344545",
                "status": "PENDING_SERVICE",
                "message": "Payment was received"
            }
        })
        message = MessageBusMessage.from_json(json_str)
        assert message.meta_data.instruction_type == "STATUS_UPDATE"
        assert message.meta_data.idempotency_key == "unique-key-456"
        assert message.payload.reference == "MYK123344545"

    def test_correction_message_from_json(self):
        """Test deserializing correction message from JSON"""
        json_str = json.dumps({
            "meta_data": {
                "source": "WATCHTOWER",
                "instruction_type": "CORRECTION",
                "created_at": "2021-01-01T00:00:00Z",
                "token": "test.token.here",
                "idempotency_key": "unique-key-789"
            },
            "payload": {
                "reference": "MYK123344545",
                "value": "2.00",
                "message": "Over paid",
                "currency": "EUR",
                "source": "BANK_WISE"
            }
        })
        message = MessageBusMessage.from_json(json_str)
        assert message.meta_data.instruction_type == "CORRECTION"
        assert message.meta_data.idempotency_key == "unique-key-789"
        assert message.payload.value == "2.00"

    def test_message_to_json(self):
        """Test serializing message to JSON"""
        message = MessageBusMessage(
            meta_data=MetaData(
                source="BANKING_SERVICE",
                instruction_type="PAYMENT",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here",
                idempotency_key="unique-key-123"
            ),
            payload=PaymentPayload(
                external_reference="P763763453G",
                payer_name="John Doe",
                currency="EUR",
                value="123.00",
                source="BANK_MODULR",
                reference="MYK123344545",
                bank_account_number="GB123266734836738787454"
            )
        )
        json_str = message.to_json()
        parsed = json.loads(json_str)
        assert parsed["meta_data"]["source"] == "BANKING_SERVICE"
        assert parsed["meta_data"]["idempotency_key"] == "unique-key-123"
        assert parsed["payload"]["external_reference"] == "P763763453G"

    def test_create_payment_message(self):
        """Test creating payment message with convenience function"""
        payload = PaymentPayload(
            external_reference="P763763453G",
            payer_name="John Doe",
            currency="EUR",
            value="123.00",
            source="BANK_MODULR",
            reference="MYK123344545",
            bank_account_number="GB123266734836738787454"
        )

        message = MessageBusMessage.create(
            source="BANKING_SERVICE",
            instruction_type="PAYMENT",
            payload=payload,
            service_token="test.token.here"
        )

        assert message.meta_data.source == "BANKING_SERVICE"
        assert message.meta_data.instruction_type == "PAYMENT"
        assert message.meta_data.token == "test.token.here"
        assert message.meta_data.idempotency_key is not None
        assert len(message.meta_data.idempotency_key) > 0
        assert message.payload == payload

        # Verify created_at format
        created_at_dt = datetime.strptime(message.meta_data.created_at, "%Y-%m-%dT%H:%M:%SZ")
        assert isinstance(created_at_dt, datetime)

    def test_create_status_update_message(self):
        """Test creating status update message with convenience function"""
        payload = StatusUpdatePayload(
            reference="MYK123344545",
            status="PENDING_SERVICE",
            message="Payment was received"
        )

        message = MessageBusMessage.create(
            source="ANCHOR_MYKOBO",
            instruction_type="STATUS_UPDATE",
            payload=payload,
            service_token="test.token.here"
        )

        assert message.meta_data.source == "ANCHOR_MYKOBO"
        assert message.meta_data.instruction_type == "STATUS_UPDATE"
        assert message.payload == payload

    def test_create_correction_message(self):
        """Test creating correction message with convenience function"""
        payload = CorrectionPayload(
            reference="MYK123344545",
            value="2.00",
            message="Over paid",
            currency="EUR",
            source="BANK_WISE"
        )

        message = MessageBusMessage.create(
            source="WATCHTOWER",
            instruction_type="CORRECTION",
            payload=payload,
            service_token="test.token.here"
        )

        assert message.meta_data.source == "WATCHTOWER"
        assert message.meta_data.instruction_type == "CORRECTION"
        assert message.payload == payload

    def test_create_message_with_custom_idempotency_key(self):
        """Test creating message with custom idempotency key"""
        payload = PaymentPayload(
            external_reference="P763763453G",
            payer_name="John Doe",
            currency="EUR",
            value="123.00",
            source="BANK_MODULR",
            reference="MYK123344545",
            bank_account_number="GB123266734836738787454"
        )

        custom_key = "my-custom-idempotency-key-123"
        message = MessageBusMessage.create(
            source="BANKING_SERVICE",
            instruction_type="PAYMENT",
            payload=payload,
            service_token="test.token.here",
            idempotency_key=custom_key
        )

        assert message.meta_data.idempotency_key == custom_key

    def test_create_message_generates_unique_idempotency_keys(self):
        """Test that auto-generated idempotency keys are unique"""
        payload = PaymentPayload(
            external_reference="P763763453G",
            payer_name="John Doe",
            currency="EUR",
            value="123.00",
            source="BANK_MODULR",
            reference="MYK123344545",
            bank_account_number="GB123266734836738787454"
        )

        message1 = MessageBusMessage.create(
            source="BANKING_SERVICE",
            instruction_type="PAYMENT",
            payload=payload,
            service_token="test.token.here"
        )

        message2 = MessageBusMessage.create(
            source="BANKING_SERVICE",
            instruction_type="PAYMENT",
            payload=payload,
            service_token="test.token.here"
        )

        assert message1.meta_data.idempotency_key != message2.meta_data.idempotency_key

    def test_create_message_with_enum_instruction_type(self):
        """Test creating message with InstructionType enum"""
        payload = PaymentPayload(
            external_reference="P763763453G",
            payer_name="John Doe",
            currency="EUR",
            value="123.00",
            source="BANK_MODULR",
            reference="MYK123344545",
            bank_account_number="GB123266734836738787454"
        )

        message = MessageBusMessage.create(
            source="BANKING_SERVICE",
            instruction_type=InstructionType.PAYMENT,
            payload=payload,
            service_token="test.token.here"
        )

        assert message.meta_data.instruction_type == InstructionType.PAYMENT
        assert isinstance(message.meta_data.instruction_type, InstructionType)

    def test_payment_instruction_requires_payment_payload(self):
        """Test that PAYMENT instruction_type requires PaymentPayload"""
        # Valid: PAYMENT with PaymentPayload
        payload = PaymentPayload(
            external_reference="P123",
            payer_name="John Doe",
            currency="EUR",
            value="100.00",
            source="BANK",
            reference="REF123",
            bank_account_number="GB123"
        )

        message = MessageBusMessage(
            meta_data=MetaData(
                source="BANKING_SERVICE",
                instruction_type=InstructionType.PAYMENT,
                created_at="2021-01-01T00:00:00Z",
                token="test.token",
                idempotency_key="key-123"
            ),
            payload=payload
        )
        assert isinstance(message.payload, PaymentPayload)

    def test_payment_instruction_rejects_wrong_payload(self):
        """Test that PAYMENT instruction_type rejects non-PaymentPayload"""
        wrong_payload = StatusUpdatePayload(
            reference="REF123",
            status="PENDING",
            message="Test"
        )

        with pytest.raises(ValueError) as exc_info:
            MessageBusMessage(
                meta_data=MetaData(
                    source="BANKING_SERVICE",
                    instruction_type=InstructionType.PAYMENT,
                    created_at="2021-01-01T00:00:00Z",
                    token="test.token",
                    idempotency_key="key-123"
                ),
                payload=wrong_payload
            )

        assert "PAYMENT requires PaymentPayload" in str(exc_info.value)
        assert "StatusUpdatePayload" in str(exc_info.value)

    def test_status_update_instruction_requires_status_update_payload(self):
        """Test that STATUS_UPDATE instruction_type requires StatusUpdatePayload"""
        # Valid: STATUS_UPDATE with StatusUpdatePayload
        payload = StatusUpdatePayload(
            reference="REF123",
            status="PENDING_SERVICE",
            message="Waiting for service"
        )

        message = MessageBusMessage(
            meta_data=MetaData(
                source="ANCHOR_MYKOBO",
                instruction_type=InstructionType.STATUS_UPDATE,
                created_at="2021-01-01T00:00:00Z",
                token="test.token",
                idempotency_key="key-456"
            ),
            payload=payload
        )
        assert isinstance(message.payload, StatusUpdatePayload)

    def test_status_update_instruction_rejects_wrong_payload(self):
        """Test that STATUS_UPDATE instruction_type rejects non-StatusUpdatePayload"""
        wrong_payload = PaymentPayload(
            external_reference="P123",
            payer_name="John Doe",
            currency="EUR",
            value="100.00",
            source="BANK",
            reference="REF123",
            bank_account_number="GB123"
        )

        with pytest.raises(ValueError) as exc_info:
            MessageBusMessage(
                meta_data=MetaData(
                    source="ANCHOR_MYKOBO",
                    instruction_type=InstructionType.STATUS_UPDATE,
                    created_at="2021-01-01T00:00:00Z",
                    token="test.token",
                    idempotency_key="key-456"
                ),
                payload=wrong_payload
            )

        assert "STATUS_UPDATE requires StatusUpdatePayload" in str(exc_info.value)
        assert "PaymentPayload" in str(exc_info.value)

    def test_correction_instruction_requires_correction_payload(self):
        """Test that CORRECTION instruction_type requires CorrectionPayload"""
        # Valid: CORRECTION with CorrectionPayload
        payload = CorrectionPayload(
            reference="REF123",
            value="50.00",
            message="Overpayment",
            currency="EUR",
            source="BANK_WISE"
        )

        message = MessageBusMessage(
            meta_data=MetaData(
                source="WATCHTOWER",
                instruction_type=InstructionType.CORRECTION,
                created_at="2021-01-01T00:00:00Z",
                token="test.token",
                idempotency_key="key-789"
            ),
            payload=payload
        )
        assert isinstance(message.payload, CorrectionPayload)

    def test_correction_instruction_rejects_wrong_payload(self):
        """Test that CORRECTION instruction_type rejects non-CorrectionPayload"""
        wrong_payload = StatusUpdatePayload(
            reference="REF123",
            status="PENDING",
            message="Test"
        )

        with pytest.raises(ValueError) as exc_info:
            MessageBusMessage(
                meta_data=MetaData(
                    source="WATCHTOWER",
                    instruction_type=InstructionType.CORRECTION,
                    created_at="2021-01-01T00:00:00Z",
                    token="test.token",
                    idempotency_key="key-789"
                ),
                payload=wrong_payload
            )

        assert "CORRECTION requires CorrectionPayload" in str(exc_info.value)
        assert "StatusUpdatePayload" in str(exc_info.value)

    def test_create_event_message(self):
        """Test creating event message with convenience function"""
        from mykobo_py.message_bus.models.event import NewTransactionEventPayload

        payload = NewTransactionEventPayload(
            created_at="2021-01-01T00:00:00Z",
            kind="DEPOSIT",
            reference="TXN123",
            source="BANKING_SERVICE"
        )

        message = MessageBusMessage.create(
            source="BANKING_SERVICE",
            payload=payload,
            service_token="test.token.here",
            event=EventType.NEW_TRANSACTION
        )

        assert message.meta_data.source == "BANKING_SERVICE"
        assert message.meta_data.event == EventType.NEW_TRANSACTION
        assert message.meta_data.instruction_type is None
        assert message.meta_data.token == "test.token.here"
        assert message.meta_data.idempotency_key is not None
        assert len(message.meta_data.idempotency_key) > 0
        assert message.payload == payload

    def test_create_event_message_with_string_event_type(self):
        """Test creating event message with string event type"""
        from mykobo_py.message_bus.models.event import NewTransactionEventPayload

        payload = NewTransactionEventPayload(
            created_at="2021-01-01T00:00:00Z",
            kind="DEPOSIT",
            reference="TXN123",
            source="BANKING_SERVICE"
        )

        message = MessageBusMessage.create(
            source="BANKING_SERVICE",
            payload=payload,
            service_token="test.token.here",
            event="NEW_TRANSACTION"
        )

        assert message.meta_data.event == EventType.NEW_TRANSACTION
        assert isinstance(message.meta_data.event, EventType)
        assert message.meta_data.instruction_type is None

    def test_create_message_requires_instruction_or_event(self):
        """Test that create method requires either instruction_type or event"""
        from mykobo_py.message_bus.models.event import NewTransactionEventPayload

        payload = NewTransactionEventPayload(
            created_at="2021-01-01T00:00:00Z",
            kind="DEPOSIT",
            reference="TXN123",
            source="BANKING_SERVICE"
        )

        with pytest.raises(ValueError) as exc_info:
            MessageBusMessage.create(
                source="BANKING_SERVICE",
                payload=payload,
                service_token="test.token.here"
            )

        assert "Either instruction_type or event must be provided" in str(exc_info.value)

    def test_create_message_rejects_both_instruction_and_event(self):
        """Test that create method rejects both instruction_type and event"""
        payload = PaymentPayload(
            external_reference="P763763453G",
            payer_name="John Doe",
            currency="EUR",
            value="123.00",
            source="BANK_MODULR",
            reference="MYK123344545",
            bank_account_number="GB123266734836738787454"
        )

        with pytest.raises(ValueError) as exc_info:
            MessageBusMessage.create(
                source="BANKING_SERVICE",
                payload=payload,
                service_token="test.token.here",
                instruction_type=InstructionType.PAYMENT,
                event=EventType.NEW_TRANSACTION
            )

        assert "Cannot specify both instruction_type and event" in str(exc_info.value)

    def test_transaction_status_update(self):
        """Test transaction_status update"""
        payload = json.dumps({
            "meta_data": {
                "source": "MYKOBO_LEDGER",
                "created_at": "2025-12-20T17:27:51Z",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46c3ZjOjI4MDc4MTY1NDdkYTQwMzE4ZmVmM2NhNDZkNWEzZjVjIiwianRpIjoidXJuOnRrbjo2YTFiZjAxODZmNzY0YTFhYmIzOGM4MTMxZTZmNGQyZCIsImlzcyI6InByZC5pZGVudGl0eS5teWtvYm8uY28iLCJpYXQiOjE3NjU5NTIxMzEsImV4cCI6MTc2NjU1NjkzMSwiYXVkIjoiU2VydmljZSIsInNjb3BlIjpbInVzZXI6cmVhZCIsInVzZXI6d3JpdGUiLCJ1c2VyOmFkbWluIiwic2VydmljZTpyZWFkIiwidG9rZW46cmVhZCIsImJ1c2luZXNzOnJlYWQiLCJidXNpbmVzczpyZWFkIiwid2FsbGV0OnJlYWQiLCJ3YWxsZXQ6d3JpdGUiLCJ0cmFuc2FjdGlvbjpyZWFkIiwidHJhbnNhY3Rpb246d3JpdGUiLCJ0cmFuc2FjdGlvbjphZG1pbiIsInBheW1lbnQ6cmVhZCIsInBheW1lbnQ6d3JpdGUiLCJwYXltZW50OmFkbWluIl19.c_0e7v-fMMWdCpown3e4hXbFKnjM2tyOV_ty827VgFA",
                "idempotency_key": "677a921e-56a6-40af-ac83-db78ca1faf00",
                "instruction_type": "STATUS_UPDATE"
            },
            "payload": {
                "reference": "1001766240984",
                "status": "FUNDS_RECEIVED",
                "message": "Payment received and applied successfully",
                "transaction_id": "c1059c63-49d7-45d9-81c4-0aaf7e263382"
            }
        })

        message = MessageBusMessage.from_json(payload)
        print(message)
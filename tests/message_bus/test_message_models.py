import pytest
import json
from mykobo_py.message_bus.models import (
    MessageBusMessage,
    MetaData,
    PaymentPayload,
    StatusUpdatePayload,
    CorrectionPayload,
)


class TestMetaData:
    """Tests for MetaData model"""

    def test_metadata_valid(self):
        """Test creating valid MetaData"""
        metadata = MetaData(
            source="BANKING_SERVICE",
            instruction_type="PAYMENT",
            created_at="2021-01-01T00:00:00Z",
            token="test.token.here"
        )
        assert metadata.source == "BANKING_SERVICE"
        assert metadata.instruction_type == "PAYMENT"
        assert metadata.created_at == "2021-01-01T00:00:00Z"
        assert metadata.token == "test.token.here"

    def test_metadata_missing_source(self):
        """Test MetaData validation fails when source is missing"""
        with pytest.raises(ValueError) as exc_info:
            MetaData(
                source="",
                instruction_type="PAYMENT",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here"
            )
        assert "MetaData missing required fields: source" in str(exc_info.value)

    def test_metadata_missing_instruction_type(self):
        """Test MetaData validation fails when instruction_type is missing"""
        with pytest.raises(ValueError) as exc_info:
            MetaData(
                source="BANKING_SERVICE",
                instruction_type=None,
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here"
            )
        assert "instruction_type" in str(exc_info.value)

    def test_metadata_missing_multiple_fields(self):
        """Test MetaData validation fails when multiple fields are missing"""
        with pytest.raises(ValueError) as exc_info:
            MetaData(
                source="",
                instruction_type="PAYMENT",
                created_at="",
                token=""
            )
        assert "source" in str(exc_info.value)
        assert "created_at" in str(exc_info.value)
        assert "token" in str(exc_info.value)

    def test_metadata_from_json(self):
        """Test deserializing MetaData from JSON"""
        json_str = json.dumps({
            "source": "BANKING_SERVICE",
            "instruction_type": "PAYMENT",
            "created_at": "2021-01-01T00:00:00Z",
            "token": "test.token.here"
        })
        metadata = MetaData.from_json(json_str)
        assert metadata.source == "BANKING_SERVICE"
        assert metadata.instruction_type == "PAYMENT"


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
                token="test.token.here"
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
        assert isinstance(message.payload, PaymentPayload)
        assert message.payload.external_reference == "P763763453G"

    def test_status_update_message_valid(self):
        """Test creating valid status update message"""
        message = MessageBusMessage(
            meta_data=MetaData(
                source="ANCHOR_MYKOBO",
                instruction_type="STATUS_UPDATE",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here"
            ),
            payload=StatusUpdatePayload(
                reference="MYK123344545",
                status="PENDING_SERVICE",
                message="Payment was received"
            )
        )
        assert message.meta_data.source == "ANCHOR_MYKOBO"
        assert isinstance(message.payload, StatusUpdatePayload)
        assert message.payload.status == "PENDING_SERVICE"

    def test_correction_message_valid(self):
        """Test creating valid correction message"""
        message = MessageBusMessage(
            meta_data=MetaData(
                source="WATCHTOWER",
                instruction_type="CORRECTION",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here"
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
        assert isinstance(message.payload, CorrectionPayload)
        assert message.payload.value == "2.00"

    def test_payment_message_from_json(self):
        """Test deserializing payment message from JSON"""
        json_str = json.dumps({
            "meta_data": {
                "source": "BANKING_SERVICE",
                "instruction_type": "PAYMENT",
                "created_at": "2021-01-01T00:00:00Z",
                "token": "test.token.here"
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
        assert message.payload.external_reference == "P763763453G"

    def test_status_update_message_from_json(self):
        """Test deserializing status update message from JSON"""
        json_str = json.dumps({
            "meta_data": {
                "source": "ANCHOR_MYKOBO",
                "instruction_type": "STATUS_UPDATE",
                "created_at": "2021-01-01T00:00:00Z",
                "token": "test.token.here"
            },
            "payload": {
                "reference": "MYK123344545",
                "status": "PENDING_SERVICE",
                "message": "Payment was received"
            }
        })
        message = MessageBusMessage.from_json(json_str)
        assert message.meta_data.instruction_type == "STATUS_UPDATE"
        assert message.payload.reference == "MYK123344545"

    def test_correction_message_from_json(self):
        """Test deserializing correction message from JSON"""
        json_str = json.dumps({
            "meta_data": {
                "source": "WATCHTOWER",
                "instruction_type": "CORRECTION",
                "created_at": "2021-01-01T00:00:00Z",
                "token": "test.token.here"
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
        assert message.payload.value == "2.00"

    def test_message_to_json(self):
        """Test serializing message to JSON"""
        message = MessageBusMessage(
            meta_data=MetaData(
                source="BANKING_SERVICE",
                instruction_type="PAYMENT",
                created_at="2021-01-01T00:00:00Z",
                token="test.token.here"
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
        assert parsed["payload"]["external_reference"] == "P763763453G"

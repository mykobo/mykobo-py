import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from mykobo_py.message_bus.sqs.SQS import SQS
from mykobo_py.message_bus.models import (
    MessageBusMessage,
    MetaData,
    PaymentPayload,
    InstructionType,
)


class TestSQS:
    """Tests for SQS class"""

    @pytest.fixture
    def sqs_client(self):
        """Create SQS client with mocked boto3 client"""
        with patch('mykobo_py.message_bus.sqs.SQS.boto3.client') as mock_client:
            mock_sqs = Mock()
            mock_client.return_value = mock_sqs
            sqs = SQS(queue_url="http://localhost:4566")
            sqs.client = mock_sqs
            yield sqs, mock_sqs

    def test_send_message_with_dict(self, sqs_client):
        """Test sending message with dictionary"""
        sqs, mock_client = sqs_client

        message_dict = {
            "meta_data": {
                "source": "BANKING_SERVICE",
                "instruction_type": "PAYMENT",
                "created_at": "2021-01-01T00:00:00Z",
                "token": "test.token",
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

        mock_client.send_message.return_value = {"MessageId": "msg-123"}

        response = sqs.send_message(message_dict, "test-queue")

        mock_client.send_message.assert_called_once()
        call_args = mock_client.send_message.call_args
        assert call_args[1]["QueueUrl"] == "http://localhost:4566/test-queue"
        assert call_args[1]["DelaySeconds"] == 10

        # Verify message body is valid JSON
        message_body = json.loads(call_args[1]["MessageBody"])
        assert message_body["meta_data"]["source"] == "BANKING_SERVICE"
        assert response["MessageId"] == "msg-123"

    def test_send_message_with_message_bus_message(self, sqs_client):
        """Test sending message with MessageBusMessage object"""
        sqs, mock_client = sqs_client

        message = MessageBusMessage(
            meta_data=MetaData(
                source="BANKING_SERVICE",
                instruction_type=InstructionType.PAYMENT,
                created_at="2021-01-01T00:00:00Z",
                token="test.token",
                idempotency_key="key-123"
            ),
            payload=PaymentPayload(
                external_reference="P123",
                payer_name="John Doe",
                currency="EUR",
                value="100.00",
                source="BANK",
                reference="REF123",
                bank_account_number="GB123"
            )
        )

        mock_client.send_message.return_value = {"MessageId": "msg-456"}

        response = sqs.send_message(message, "test-queue")

        mock_client.send_message.assert_called_once()
        call_args = mock_client.send_message.call_args
        assert call_args[1]["QueueUrl"] == "http://localhost:4566/test-queue"
        assert call_args[1]["DelaySeconds"] == 10

        # Verify message body is valid JSON and contains expected data
        message_body = json.loads(call_args[1]["MessageBody"])
        assert message_body["meta_data"]["source"] == "BANKING_SERVICE"
        assert message_body["meta_data"]["instruction_type"] == "PAYMENT"
        assert message_body["meta_data"]["idempotency_key"] == "key-123"
        assert message_body["payload"]["external_reference"] == "P123"
        assert message_body["payload"]["currency"] == "EUR"
        assert response["MessageId"] == "msg-456"

    def test_send_message_with_convenience_function(self, sqs_client):
        """Test sending message created with convenience function"""
        sqs, mock_client = sqs_client

        payload = PaymentPayload(
            external_reference="P789",
            payer_name="Jane Doe",
            currency="GBP",
            value="250.00",
            source="BANK_WISE",
            reference="REF789",
            bank_account_number="GB456"
        )

        message = MessageBusMessage.create(
            source="BANKING_SERVICE",
            instruction_type=InstructionType.PAYMENT,
            payload=payload,
            service_token="jwt.token.here",
            idempotency_key="custom-key-789"
        )

        mock_client.send_message.return_value = {"MessageId": "msg-789"}

        response = sqs.send_message(message, "payment-queue")

        mock_client.send_message.assert_called_once()
        call_args = mock_client.send_message.call_args

        # Verify message body
        message_body = json.loads(call_args[1]["MessageBody"])
        assert message_body["meta_data"]["source"] == "BANKING_SERVICE"
        assert message_body["meta_data"]["instruction_type"] == "PAYMENT"
        assert message_body["meta_data"]["idempotency_key"] == "custom-key-789"
        assert message_body["meta_data"]["token"] == "jwt.token.here"
        assert message_body["payload"]["external_reference"] == "P789"
        assert message_body["payload"]["value"] == "250.00"

    def test_send_message_backward_compatibility(self, sqs_client):
        """Test that process parameter is still accepted for backward compatibility"""
        sqs, mock_client = sqs_client

        message_dict = {"test": "data"}
        mock_client.send_message.return_value = {"MessageId": "msg-999"}

        # Should not raise error even with deprecated process parameter
        response = sqs.send_message(message_dict, "test-queue", process="legacy-process")

        mock_client.send_message.assert_called_once()
        assert response["MessageId"] == "msg-999"

    def test_send_message_queue_url_construction(self, sqs_client):
        """Test that queue URL is constructed correctly"""
        sqs, mock_client = sqs_client

        message = {"test": "data"}
        mock_client.send_message.return_value = {"MessageId": "msg-url"}

        sqs.send_message(message, "my-queue")

        call_args = mock_client.send_message.call_args
        assert call_args[1]["QueueUrl"] == "http://localhost:4566/my-queue"

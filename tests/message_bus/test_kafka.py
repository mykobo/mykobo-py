import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from kafka import TopicPartition
from mykobo_py.message_bus.kafka.kafka import Kafka
from mykobo_py.message_bus.models import (
    MessageBusMessage,
    MetaData,
    PaymentPayload,
    InstructionType,
)


class TestKafka:
    """Tests for Kafka class"""

    @pytest.fixture
    def kafka_client(self):
        """Create Kafka client with mocked KafkaProducer and KafkaConsumer"""
        with patch('mykobo_py.message_bus.kafka.kafka.KafkaProducer') as mock_producer_class, \
             patch('mykobo_py.message_bus.kafka.kafka.KafkaConsumer') as mock_consumer_class:

            mock_producer = Mock()
            mock_producer_class.return_value = mock_producer

            kafka = Kafka(bootstrap_servers="localhost:9092")

            yield kafka, mock_producer, mock_consumer_class

    def test_init_with_string_bootstrap_servers(self):
        """Test initialization with string bootstrap servers"""
        kafka = Kafka(bootstrap_servers="localhost:9092,localhost:9093")
        assert kafka.bootstrap_servers == ["localhost:9092", "localhost:9093"]

    def test_init_with_list_bootstrap_servers(self):
        """Test initialization with list bootstrap servers"""
        kafka = Kafka(bootstrap_servers=["localhost:9092", "localhost:9093"])
        assert kafka.bootstrap_servers == ["localhost:9092", "localhost:9093"]

    def test_init_with_env_var(self):
        """Test initialization with environment variable"""
        with patch.dict('os.environ', {'KAFKA_BOOTSTRAP_SERVERS': 'kafka1:9092,kafka2:9092'}):
            kafka = Kafka()
            assert kafka.bootstrap_servers == ["kafka1:9092", "kafka2:9092"]

    def test_init_default_bootstrap_servers(self):
        """Test initialization with default bootstrap servers"""
        with patch.dict('os.environ', {}, clear=True):
            kafka = Kafka()
            assert kafka.bootstrap_servers == ["localhost:9092"]

    def test_init_with_authentication_params(self):
        """Test initialization with authentication parameters"""
        kafka = Kafka(
            bootstrap_servers="localhost:9092",
            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",
            user_name="test_user",
            password="test_password"
        )
        assert kafka.security_protocol == "SASL_SSL"
        assert kafka.sasl_mechanism == "PLAIN"
        assert kafka.user_name == "test_user"
        assert kafka.password == "test_password"

    def test_init_default_authentication_params(self):
        """Test initialization with default authentication parameters"""
        kafka = Kafka(bootstrap_servers="localhost:9092")
        assert kafka.security_protocol == "SASL_SSL"
        assert kafka.sasl_mechanism == "PLAIN"
        assert kafka.user_name is None
        assert kafka.password is None

    def test_send_message_with_dict(self, kafka_client):
        """Test sending message with dictionary"""
        kafka, mock_producer, _ = kafka_client

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

        # Mock the future returned by send
        mock_future = Mock()
        mock_metadata = Mock()
        mock_metadata.partition = 0
        mock_metadata.offset = 42
        mock_future.get.return_value = mock_metadata
        mock_producer.send.return_value = mock_future

        result = kafka.send_message(message_dict, "test-topic")

        mock_producer.send.assert_called_once()
        call_args = mock_producer.send.call_args
        assert call_args[1]["topic"] == "test-topic"
        assert call_args[1]["value"] == message_dict
        assert call_args[1]["key"] is None
        assert result.partition == 0
        assert result.offset == 42

    def test_send_message_with_message_bus_message(self, kafka_client):
        """Test sending message with MessageBusMessage object"""
        kafka, mock_producer, _ = kafka_client

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

        mock_future = Mock()
        mock_metadata = Mock()
        mock_metadata.partition = 1
        mock_metadata.offset = 100
        mock_future.get.return_value = mock_metadata
        mock_producer.send.return_value = mock_future

        result = kafka.send_message(message, "payment-topic")

        mock_producer.send.assert_called_once()
        call_args = mock_producer.send.call_args
        assert call_args[1]["topic"] == "payment-topic"

        # Verify the message was serialized correctly
        sent_value = call_args[1]["value"]
        assert sent_value["meta_data"]["source"] == "BANKING_SERVICE"
        assert sent_value["meta_data"]["instruction_type"] == "PAYMENT"
        assert sent_value["payload"]["external_reference"] == "P123"
        assert result.offset == 100

    def test_send_message_with_key(self, kafka_client):
        """Test sending message with partition key"""
        kafka, mock_producer, _ = kafka_client

        message_dict = {"test": "data"}

        mock_future = Mock()
        mock_metadata = Mock()
        mock_metadata.partition = 2
        mock_metadata.offset = 50
        mock_future.get.return_value = mock_metadata
        mock_producer.send.return_value = mock_future

        kafka.send_message(message_dict, "test-topic", key="user-123")

        call_args = mock_producer.send.call_args
        assert call_args[1]["key"] == "user-123"


    def test_send_message_kafka_error(self, kafka_client):
        """Test handling of Kafka errors during send"""
        kafka, mock_producer, _ = kafka_client

        from kafka.errors import KafkaError

        mock_future = Mock()
        mock_future.get.side_effect = KafkaError("Connection failed")
        mock_producer.send.return_value = mock_future

        with pytest.raises(KafkaError):
            kafka.send_message({"test": "data"}, "test-topic")

    def test_receive_message_success(self, kafka_client):
        """Test successfully receiving a message"""
        kafka, _, mock_consumer_class = kafka_client

        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer

        # Mock a received message
        mock_record = Mock()
        mock_record.value = {"test": "data", "message_id": "123"}
        mock_record.offset = 42

        mock_partition = TopicPartition("test-topic", 0)
        mock_consumer.poll.return_value = {
            mock_partition: [mock_record]
        }

        result = kafka.receive_message("test-topic", group_id="test-group")

        assert result is not None
        receipt_handle, message_body = list(result.items())[0]
        assert receipt_handle == "test-topic:0:42"
        assert message_body == {"test": "data", "message_id": "123"}

        # Verify consumer was created with correct parameters
        mock_consumer_class.assert_called_once()
        call_args = mock_consumer_class.call_args
        assert "test-topic" in call_args[0]
        assert call_args[1]["group_id"] == "test-group"
        assert call_args[1]["bootstrap_servers"] == ["localhost:9092"]

    def test_receive_message_no_messages(self, kafka_client):
        """Test receiving when no messages are available"""
        kafka, _, mock_consumer_class = kafka_client

        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer
        mock_consumer.poll.return_value = {}

        result = kafka.receive_message("test-topic")

        assert result is None

    def test_receive_message_default_group_id(self, kafka_client):
        """Test receiving message with default group ID"""
        kafka, _, mock_consumer_class = kafka_client

        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer
        mock_consumer.poll.return_value = {}

        kafka.receive_message("my-topic")

        call_args = mock_consumer_class.call_args
        assert call_args[1]["group_id"] == "my-topic_consumer_group"

    def test_receive_message_reuses_consumer(self, kafka_client):
        """Test that consumer is reused for same topic/group"""
        kafka, _, mock_consumer_class = kafka_client

        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer
        mock_consumer.poll.return_value = {}

        kafka.receive_message("test-topic", group_id="test-group")
        kafka.receive_message("test-topic", group_id="test-group")

        # Consumer should only be created once
        mock_consumer_class.assert_called_once()
        # Poll should be called twice
        assert mock_consumer.poll.call_count == 2

    def test_receive_message_different_consumers(self, kafka_client):
        """Test that different consumers are created for different topic/group combinations"""
        kafka, _, mock_consumer_class = kafka_client

        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer
        mock_consumer.poll.return_value = {}

        kafka.receive_message("topic1", group_id="group1")
        kafka.receive_message("topic2", group_id="group2")

        # Two different consumers should be created
        assert mock_consumer_class.call_count == 2

    def test_receive_message_exception_handling(self, kafka_client):
        """Test exception handling during receive"""
        kafka, _, mock_consumer_class = kafka_client

        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer
        mock_consumer.poll.side_effect = Exception("Consumer error")

        result = kafka.receive_message("test-topic")

        assert result is None

    def test_commit_offset_success(self, kafka_client):
        """Test successfully committing offset"""
        kafka, _, mock_consumer_class = kafka_client

        # First receive a message to create consumer
        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer

        mock_record = Mock()
        mock_record.value = {"test": "data"}
        mock_record.offset = 42
        mock_partition = TopicPartition("test-topic", 0)
        mock_consumer.poll.return_value = {mock_partition: [mock_record]}

        result = kafka.receive_message("test-topic", group_id="test-group")
        receipt_handle = list(result.keys())[0]

        # Now commit the offset
        kafka.commit_offset("test-topic", receipt_handle)

        # Verify commit was called
        mock_consumer.commit.assert_called_once()
        commit_args = mock_consumer.commit.call_args[0][0]

        # Should commit offset 43 (next offset after 42)
        assert TopicPartition("test-topic", 0) in commit_args
        assert commit_args[TopicPartition("test-topic", 0)].offset == 43

    def test_commit_offset_invalid_receipt_handle(self, kafka_client):
        """Test commit_offset with invalid receipt handle format"""
        kafka, _, _ = kafka_client

        # Should not raise exception, just log error
        kafka.commit_offset("test-topic", "invalid-format")

    def test_commit_offset_no_consumer(self, kafka_client):
        """Test commit_offset when no consumer exists for the topic"""
        kafka, _, _ = kafka_client

        # Should not raise exception, just log warning
        kafka.commit_offset("test-topic", "test-topic:0:42")

    def test_close(self, kafka_client):
        """Test closing all connections"""
        kafka, mock_producer, mock_consumer_class = kafka_client

        # Create a consumer
        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer
        mock_consumer.poll.return_value = {}
        kafka.receive_message("test-topic")

        # Access producer to initialize it
        _ = kafka.producer

        # Close all connections
        kafka.close()

        mock_producer.close.assert_called_once()
        mock_consumer.close.assert_called_once()

    def test_send_message_with_convenience_function(self, kafka_client):
        """Test sending message created with convenience function"""
        kafka, mock_producer, _ = kafka_client

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

        mock_future = Mock()
        mock_metadata = Mock()
        mock_metadata.partition = 0
        mock_metadata.offset = 1
        mock_future.get.return_value = mock_metadata
        mock_producer.send.return_value = mock_future

        kafka.send_message(message, "payment-topic")

        call_args = mock_producer.send.call_args
        sent_value = call_args[1]["value"]

        assert sent_value["meta_data"]["source"] == "BANKING_SERVICE"
        assert sent_value["meta_data"]["instruction_type"] == "PAYMENT"
        assert sent_value["meta_data"]["idempotency_key"] == "custom-key-789"
        assert sent_value["meta_data"]["token"] == "jwt.token.here"
        assert sent_value["payload"]["external_reference"] == "P789"
        assert sent_value["payload"]["value"] == "250.00"

    def test_lazy_producer_initialization(self, kafka_client):
        """Test that producer is only created when first needed"""
        kafka, mock_producer, _ = kafka_client

        # Producer should not be created yet
        assert kafka._producer is None

        # Access producer property
        producer = kafka.producer

        # Now it should be created
        assert kafka._producer is not None
        assert producer == mock_producer

    def test_consumer_timeout_configuration(self, kafka_client):
        """Test that consumer timeout is configurable"""
        kafka, _, mock_consumer_class = kafka_client

        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer
        mock_consumer.poll.return_value = {}

        kafka.receive_message("test-topic", timeout_ms=5000)

        call_args = mock_consumer_class.call_args
        assert call_args[1]["consumer_timeout_ms"] == 5000

    def test_auto_commit_configuration(self, kafka_client):
        """Test that auto_commit can be configured"""
        kafka, _, mock_consumer_class = kafka_client

        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer
        mock_consumer.poll.return_value = {}

        kafka.receive_message("test-topic", auto_commit=True)

        call_args = mock_consumer_class.call_args
        assert call_args[1]["enable_auto_commit"] is True

    def test_producer_authentication_configuration(self):
        """Test that producer is initialized with authentication parameters"""
        with patch('mykobo_py.message_bus.kafka.kafka.KafkaProducer') as mock_producer_class:
            mock_producer = Mock()
            mock_producer_class.return_value = mock_producer

            kafka = Kafka(
                bootstrap_servers="kafka.example.com:9092",
                security_protocol="SASL_SSL",
                sasl_mechanism="SCRAM-SHA-256",
                user_name="my_user",
                password="my_password"
            )

            # Access producer to trigger initialization
            _ = kafka.producer

            # Verify producer was created with correct auth params
            mock_producer_class.assert_called_once()
            call_args = mock_producer_class.call_args
            assert call_args[1]["bootstrap_servers"] == ["kafka.example.com:9092"]
            assert call_args[1]["security_protocol"] == "SASL_SSL"
            assert call_args[1]["sasl_mechanism"] == "SCRAM-SHA-256"
            assert call_args[1]["sasl_plain_username"] == "my_user"
            assert call_args[1]["sasl_plain_password"] == "my_password"
            assert call_args[1]["acks"] == 'all'
            assert call_args[1]["retries"] == 3

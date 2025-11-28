import os
import logging
from typing import Optional, Any, Dict, Union, List
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError


class Kafka:
    bootstrap_servers: List[str]
    logger = logging.getLogger(__name__)

    def __init__(self, bootstrap_servers: Optional[Union[str, List[str]]] = None, **kwargs):
        """
        Initialize Kafka client.

        Args:
            bootstrap_servers: Kafka broker addresses. Can be a string (single broker) or list.
            If not provided, will try to get from KAFKA_BOOTSTRAP_SERVERS env var.
        Keyword Args:
            consumer_id: The id for the consumer
            producer_id: The id for the producer
            security_protocol: Usually SASL_SSL or SASL_MECHANISM
            sasl_mechanism: Usually PLAIN
            user_name: Username to connect to Kafka broker
            password:  to connect to Kafka broker
        """
        if bootstrap_servers is None:
            servers_str = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
            self.bootstrap_servers = [s.strip() for s in servers_str.split(",")]
        elif isinstance(bootstrap_servers, str):
            self.bootstrap_servers = [s.strip() for s in bootstrap_servers.split(",")]
        else:
            self.bootstrap_servers = bootstrap_servers

        self.logger.debug(f"KAFKA_BOOTSTRAP_SERVERS: {self.bootstrap_servers}")

        self._producer = None
        self._consumers = {}
        self.producer_id = kwargs.get("producer_id", None)
        self.consumer_id = kwargs.get("consumer_id", None)
        self.security_protocol = kwargs.get("security_protocol", "SASL_SSL")
        self.sasl_mechanism = kwargs.get("sasl_mechanism", "PLAIN")
        self.user_name = kwargs.get("user_name", None)
        self.password = kwargs.get("password", None)

    @property
    def producer(self) -> KafkaProducer:
        """Lazily initialize and return the Kafka producer."""
        if self._producer is None:
            self._producer = KafkaProducer(
                client_id=self.producer_id,
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                security_protocol=self.security_protocol ,
                sasl_mechanism=self.sasl_mechanism,
                sasl_plain_username=self.user_name,
                sasl_plain_password=self.password,
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=1
            )
        return self._producer

    def send_message(
        self,
        message: Union['MessageBusMessage', Dict[str, Any]],
        topic: str,
        key: Optional[str] = None
    ):
        """
        Send a message to a Kafka topic.

        Args:
            message: MessageBusMessage object or dictionary to send
            topic: Name of the Kafka topic
            key: Optional message key for partitioning

        Returns:
            RecordMetadata future from Kafka
        """
        # Import here to avoid circular dependency
        from mykobo_py.message_bus.models import MessageBusMessage

        # Convert MessageBusMessage to dict if needed
        if isinstance(message, MessageBusMessage):
            message_dict = json.loads(message.to_json())
        else:
            message_dict = message

        try:
            future = self.producer.send(
                topic=topic,
                value=message_dict,
                key=key
            )
            # Block until message is sent or error occurs
            record_metadata = future.get(timeout=10)
            self.logger.debug(
                f"Message sent to topic {topic}, "
                f"partition {record_metadata.partition}, "
                f"offset {record_metadata.offset}"
            )
            return record_metadata
        except KafkaError as e:
            self.logger.error(f"Failed to send message to topic {topic}: {e}")
            raise

    def receive_message(
        self,
        topic: str,
        group_id: Optional[str] = None,
        timeout_ms: int = 1000,
        auto_commit: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Receive a single message from a Kafka topic.

        Args:
            topic: Name of the Kafka topic
            group_id: Consumer group ID. If not provided, uses a default group
            timeout_ms: Maximum time to wait for a message
            auto_commit: Whether to automatically commit offsets

        Returns:
            Dictionary with message offset as key and message body as value,
            similar to SQS format: {offset: message_dict}
            Returns None if no message available
        """
        try:
            # Get or create consumer for this topic/group
            consumer_key = f"{topic}:{group_id or 'default'}"

            if consumer_key not in self._consumers:
                actual_group_id = group_id or f"{topic}_consumer_group"
                consumer = KafkaConsumer(
                    topic,
                    client_id=self.consumer_id,
                    bootstrap_servers=self.bootstrap_servers,
                    group_id=actual_group_id,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    auto_offset_reset='earliest',
                    enable_auto_commit=auto_commit,
                    consumer_timeout_ms=timeout_ms,
                    security_protocol=self.security_protocol,
                    sasl_mechanism=self.sasl_mechanism,
                    sasl_plain_username=self.user_name,
                    sasl_plain_password=self.password,
                )
                self._consumers[consumer_key] = consumer

            consumer = self._consumers[consumer_key]

            messages = consumer.poll(timeout_ms=timeout_ms, max_records=1)

            if messages:
                for topic_partition, records in messages.items():
                    if records:
                        record = records[0]
                        # Return in SQS-like format: {receipt_handle: message_body}
                        # Using offset as the "receipt handle"
                        receipt_handle = f"{topic_partition.topic}:{topic_partition.partition}:{record.offset}"
                        return {receipt_handle: record.value}
            return None

        except Exception as e:
            self.logger.error(f"Could not receive message from topic {topic}: {e}")
            return None

    def commit_offset(self, topic: str, receipt_handle: str):
        """
        Commit the offset for a consumed message.

        Args:
            topic: Name of the Kafka topic
            receipt_handle: The receipt handle from receive_message (format: "topic:partition:offset")
        """
        try:
            # Parse the receipt handle
            parts = receipt_handle.split(":")
            if len(parts) != 3:
                self.logger.error(f"Invalid receipt handle format: {receipt_handle}")
                return

            topic_name, partition_str, offset_str = parts
            partition = int(partition_str)
            offset = int(offset_str)

            # Find the consumer that handled this message
            consumer_key = None
            for key in self._consumers:
                if key.startswith(f"{topic}:"):
                    consumer_key = key
                    break

            if not consumer_key or consumer_key not in self._consumers:
                self.logger.warning(
                    f"No consumer found for topic {topic} to commit offset"
                )
                return

            consumer = self._consumers[consumer_key]

            # Commit the offset (offset + 1 because we want to commit the next offset)
            from kafka import TopicPartition, OffsetAndMetadata

            tp = TopicPartition(topic_name, partition)
            consumer.commit({tp: OffsetAndMetadata(offset + 1, "", -1)})

            self.logger.debug(
                f"Committed offset {offset + 1} for {topic} partition {partition}"
            )

        except Exception as e:
            self.logger.error(f"Failed to commit offset: {e}")

    def close(self):
        """Close all Kafka connections."""
        if self._producer:
            self._producer.close()
            self._producer = None

        for consumer in self._consumers.values():
            consumer.close()

        self._consumers.clear()
        self.logger.debug("Closed all Kafka connections")

    def __del__(self):
        """Cleanup when object is destroyed."""
        self.close()

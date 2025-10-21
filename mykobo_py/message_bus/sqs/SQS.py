import boto3
import logging
from typing import Optional, Any, Dict
import json

class SQS:
    queue_url: Optional[str]
    logger = logging.getLogger('interactive_ui.message_bus')

    def __init__(self, queue_url: str):
        self.logger.debug("QUEUE_URL: {}".format(queue_url))
        self.queue_url = queue_url
        self.client = boto3.client('sqs', endpoint_url=queue_url)

    def send_message(self, message: Dict[str, Any], target_queue: str, process: str):
        response = self.client.send_message(
            QueueUrl=f"{self.queue_url}/{target_queue}",
            DelaySeconds=10,
            MessageBody=json.dumps(message)
        )
        return response

    def delete_message(self, target_queue: str, receipt_handle: str):
        self.client.delete_message(
            QueueUrl=f"{self.queue_url}/{target_queue}",
            ReceiptHandle=receipt_handle
        )

    def receive_message(self, target_queue: str) -> Optional[Dict[str, Any]]:
        try:
            msg = self.client.receive_message(
                QueueUrl=f"{self.queue_url}/{target_queue}",
                AttributeNames=[
                    "SentTimestamp",
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    "MYKOBO.SourceSystem",
                    "MYKOBO.Process",
                    "MYKOBO.Token",
                    "MYKOBO.Operation",
                    "MYKOBO.Channel",
                    "MYKOBO.MessageClass"
                ],
                VisibilityTimeout=0,
                WaitTimeSeconds=0,
            )
            if msg and "Messages" in msg and len(msg["Messages"]) > 0:
                return {msg["Messages"][0]["ReceiptHandle"]: json.loads(msg["Messages"][0]['Body'])}
        except KeyError as e:
            self.logger.error(f"Could not process message, key not found: {e}")
        except Exception as e:
            self.logger.error(f"Could not process message {e}")

from datetime import datetime, timedelta, timezone
from typing import Optional

from mykobo_py.message_bus.models.base import EventType


class IdempotencyKey:
    """Helpers for building deterministic idempotency keys for notifications.

    These are producer-side utilities. The keys are stored on
    circle.outbox_messages.idempotency_key (unique index) and reused as the
    Kafka message key.
    """

    @staticmethod
    def for_event(*, producer: str, event: EventType, subject_id: str) -> str:
        return f"{producer}:{event.value.lower()}:{subject_id}"

    @staticmethod
    def for_bucket(
        *,
        producer: str,
        event: EventType,
        subject_id: Optional[str],
        window: timedelta,
        now: Optional[datetime] = None,
    ) -> str:
        if now is None:
            now = datetime.now(timezone.utc)
        if now.tzinfo is None:
            raise ValueError("for_bucket requires a timezone-aware datetime")
        window_secs = int(window.total_seconds())
        if window_secs <= 0:
            raise ValueError("window must be a positive whole-second duration")
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        delta = now - epoch
        floored_seconds = (int(delta.total_seconds()) // window_secs) * window_secs
        bucket = (epoch + timedelta(seconds=floored_seconds)).isoformat()
        segments = [producer, event.value.lower()]
        if subject_id is not None:
            segments.append(subject_id)
        segments.append(bucket)
        return ":".join(segments)

from datetime import datetime, timedelta, timezone

import pytest

from mykobo_py.message_bus.models.base import EventType
from mykobo_py.notification import IdempotencyKey


def test_for_event_with_subject():
    k = IdempotencyKey.for_event(
        producer="circle", event=EventType.RELAY_INITIATED, subject_id="abc-123"
    )
    assert k == "circle:relay_initiated:abc-123"


def test_for_event_lowercases_event_value():
    k = IdempotencyKey.for_event(
        producer="circle", event=EventType.RELAY_FORWARDING_FAILED, subject_id="r-1"
    )
    assert k == "circle:relay_forwarding_failed:r-1"


def test_for_bucket_with_subject():
    now = datetime(2026, 5, 30, 12, 34, 0, tzinfo=timezone.utc)
    k = IdempotencyKey.for_bucket(
        producer="circle",
        event=EventType.RELAY_STUCK_DEPOSITING,
        subject_id="abc-123",
        window=timedelta(hours=1),
        now=now,
    )
    assert k == "circle:relay_stuck_depositing:abc-123:2026-05-30T12:00:00+00:00"


def test_for_bucket_without_subject_skips_segment():
    now = datetime(2026, 5, 30, 12, 30, 0, tzinfo=timezone.utc)
    k = IdempotencyKey.for_bucket(
        producer="circle",
        event=EventType.CIRCLE_API_5XX_BURST,
        subject_id=None,
        window=timedelta(minutes=15),
        now=now,
    )
    assert k == "circle:circle_api_5xx_burst:2026-05-30T12:30:00+00:00"


def test_for_bucket_collapses_within_window():
    base = datetime(2026, 5, 30, 12, 0, 0, tzinfo=timezone.utc)
    k1 = IdempotencyKey.for_bucket(
        producer="circle", event=EventType.RELAY_STUCK_DEPOSITING, subject_id="r-1",
        window=timedelta(hours=1), now=base + timedelta(minutes=5),
    )
    k2 = IdempotencyKey.for_bucket(
        producer="circle", event=EventType.RELAY_STUCK_DEPOSITING, subject_id="r-1",
        window=timedelta(hours=1), now=base + timedelta(minutes=55),
    )
    assert k1 == k2


def test_for_bucket_distinct_across_windows():
    base = datetime(2026, 5, 30, 12, 0, 0, tzinfo=timezone.utc)
    k1 = IdempotencyKey.for_bucket(
        producer="circle", event=EventType.RELAY_STUCK_DEPOSITING, subject_id="r-1",
        window=timedelta(hours=1), now=base + timedelta(minutes=30),
    )
    k2 = IdempotencyKey.for_bucket(
        producer="circle", event=EventType.RELAY_STUCK_DEPOSITING, subject_id="r-1",
        window=timedelta(hours=1), now=base + timedelta(hours=1, minutes=30),
    )
    assert k1 != k2


def test_for_bucket_requires_aware_datetime():
    with pytest.raises(ValueError):
        IdempotencyKey.for_bucket(
            producer="circle", event=EventType.RELAY_STUCK_DEPOSITING, subject_id="r-1",
            window=timedelta(hours=1), now=datetime(2026, 5, 30, 12, 0, 0),
        )


def test_for_bucket_rejects_zero_window():
    with pytest.raises(ValueError):
        IdempotencyKey.for_bucket(
            producer="circle", event=EventType.RELAY_STUCK_DEPOSITING, subject_id="r-1",
            window=timedelta(0),
            now=datetime(2026, 5, 30, 12, 0, 0, tzinfo=timezone.utc),
        )


def test_for_bucket_rejects_subsecond_window():
    with pytest.raises(ValueError):
        IdempotencyKey.for_bucket(
            producer="circle", event=EventType.RELAY_STUCK_DEPOSITING, subject_id="r-1",
            window=timedelta(milliseconds=500),
            now=datetime(2026, 5, 30, 12, 0, 0, tzinfo=timezone.utc),
        )

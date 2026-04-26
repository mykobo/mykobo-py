from datetime import datetime
from decimal import Decimal
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel

from .common import Chain, EnrichmentStrategy, TransactionStatus


class WatchedAddress(BaseModel):
    id: UUID
    chain: Chain
    address: str
    label: str
    enabled: bool
    token_filter: List[str]
    enrichment_strategy: EnrichmentStrategy
    dispatch_topic: str
    payload_source: str
    max_dispatch_retries: int
    created_by: str
    created_at: datetime
    updated_at: datetime


class ChainTransaction(BaseModel):
    id: UUID
    chain: Chain
    tx_hash: str
    sender: str
    recipient: str
    amount: Decimal
    token: str
    block_number: Optional[int] = None
    memo: Optional[str] = None
    status: TransactionStatus
    dispatch_retries: int
    failure_reason: Optional[str] = None
    raw_data: Optional[Any] = None
    received_at: datetime
    dispatched_at: Optional[datetime] = None


class Intent(BaseModel):
    id: UUID
    chain: Chain
    target_address: str
    expected_sender: str
    expected_amount: Decimal
    expected_token: str
    reference: str
    source: str
    matched: bool
    chain_transaction_id: Optional[UUID] = None
    expires_at: datetime
    created_at: datetime

from typing import List, Optional

from pydantic import BaseModel

from .common import Chain, EnrichmentStrategy


class CreateWatchedAddressRequest(BaseModel):
    chain: Chain
    address: str
    label: str
    enabled: Optional[bool] = None
    token_filter: Optional[List[str]] = None
    enrichment_strategy: EnrichmentStrategy
    dispatch_topic: str
    payload_source: str
    max_dispatch_retries: Optional[int] = None
    created_by: str


class UpdateWatchedAddressRequest(BaseModel):
    enabled: Optional[bool] = None
    label: Optional[str] = None
    token_filter: Optional[List[str]] = None
    dispatch_topic: Optional[str] = None
    payload_source: Optional[str] = None
    max_dispatch_retries: Optional[int] = None

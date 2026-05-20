from typing import Optional

from pydantic import BaseModel


class FeeConfiguration(BaseModel):
    transaction_type: str
    fee_rate: float
    effective_from: str
    client_domain: str
    effective_until: Optional[str]
    created_by: str
    change_reason: str


class TransactionLimitConfiguration(BaseModel):
    transaction_type: str
    asset: str
    min_amount: str
    max_amount: str
    user_id: Optional[str] = None
    client_domain: Optional[str] = None
    effective_from: Optional[str] = None
    effective_until: Optional[str] = None
    change_reason: Optional[str] = None

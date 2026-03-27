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

from typing import Optional

from pydantic import BaseModel


class CreateReferenceRequest(BaseModel):
    profile_id: str
    wallet_address: str
    client_domain: Optional[str] = None


class ReferenceResponse(BaseModel):
    id: str
    profile_id: str
    reference: str
    is_active: bool
    wallet_address: str
    client_domain: Optional[str] = None
    created_at: str

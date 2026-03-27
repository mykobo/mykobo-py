from typing import List, Optional

from pydantic import BaseModel


class TransactionFilterRequest(BaseModel):
    sources: List[str]
    transaction_types: List[str]
    statuses: List[str]
    currencies: List[str]
    from_date: Optional[str]
    to_date: Optional[str]
    payee: Optional[str]
    payer: Optional[str]
    page: int
    limit: int

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class GetVerificationExceptionRequest(BaseModel):
    user_id: Optional[str]
    from_date: Optional[str]
    to_date: Optional[str]
    verifier_type: List[str]
    created_by: Optional[str]
    page: int
    limit: int

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class AddVerificationException(BaseModel):
    user_id: str
    verifier_type: str
    error_code: str
    reason: str
    created_by: str
    expires_at: Optional[str]

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class RevokeExceptionRequest(BaseModel):
    id: int
    revoked_by: str

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

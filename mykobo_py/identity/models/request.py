from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CustomerRequest(BaseModel):
    id: Optional[str] = None
    account: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    additional_name: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    mobile_number: Optional[str] = None
    birth_date: Optional[str] = None
    birth_country_code: Optional[str] = None
    id_country_code: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_number: Optional[str] = None
    tax_id: Optional[str] = None
    tax_id_name: Optional[str] = None
    credential_id: Optional[str] = None

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class UpdateProfileRequest(BaseModel):
    bank_account_number: Optional[str] = None
    bank_number: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    id_country_code: Optional[str] = None
    tax_id: Optional[str] = None
    tax_id_name: Optional[str] = None
    suspended_at: Optional[str] = None
    deleted_at: Optional[str] = None

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class NewDocumentRequest(BaseModel):
    profile_id: str
    document_type: str
    document_status: str
    document_path: Optional[str] = None
    updated_at: Optional[str] = None
    document_sub_type: Optional[str] = None
    created_at: str = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class NewKycReviewRequest(BaseModel):
    profile_id: str
    level: str

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class UserProfileFilterRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    bank_account_number: Optional[str] = None
    id_country_code: Optional[str] = None
    suspended_at: Optional[str] = None
    deleted_at: Optional[str] = None
    page: int = 1
    limit: int = 10

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class UserRiskResetRequest(BaseModel):
    comments: Optional[str] = None

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

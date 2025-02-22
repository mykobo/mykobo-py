from dataclasses import dataclass
from datetime import datetime

from dataclasses_json.api import dataclass_json

from mykobo_py.utils import del_none
from typing import Optional

@dataclass_json
@dataclass
class CustomerRequest:
    id: Optional[str]
    account: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email_address: Optional[str]
    additional_name: Optional[str]
    address: Optional[str]
    mobile_number: Optional[str]
    birth_date: Optional[str]
    birth_country_code: Optional[str]
    id_country_code: Optional[str]
    bank_account_number: Optional[str]
    tax_id: Optional[str]
    tax_id_name: Optional[str]
    credential_id: Optional[str]

    @property
    def to_dict(self):
        return del_none(self.to_dict())

@dataclass_json
@dataclass
class UpdateProfileRequest:
    bank_account_number: Optional[str]
    tax_id: Optional[str]
    tax_id_name: Optional[str]
    suspended_at: Optional[str]
    deleted_at: Optional[str]

    @property
    def to_dict(self):
        return del_none(self.to_dict())

@dataclass_json
@dataclass
class NewDocumentRequest:
    profile_id: str
    document_type: str
    document_status: str
    document_path: Optional[str]
    updated_at: Optional[str]
    document_sub_type: Optional[str]
    created_at: str = datetime.now().isoformat()

    @property
    def to_dict(self):
        return del_none(self.to_dict())

@dataclass_json
@dataclass
class NewKycReviewRequest:
    profile_id: str
    level: str

    @property
    def to_dict(self):
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class UserProfileFilterRequest:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    bank_account_number: Optional[str] = None
    id_country_code: Optional[str] = None
    suspended_at: Optional[str] = None
    deleted_at: Optional[str] = None
    page: int = 1
    limit: int = 10

    @property
    def to_dict(self):
        return del_none(self.to_dict())

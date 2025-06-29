from dataclasses import dataclass
from datetime import datetime

from dataclasses_json.api import dataclass_json

from mykobo_py.utils import del_none
from typing import Optional

@dataclass_json
@dataclass
class CustomerRequest:
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

    @property
    def to_dict(self):
        return del_none(self.to_dict())

@dataclass_json
@dataclass
class UpdateProfileRequest:
    bank_account_number: Optional[str]
    bank_number: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    id_country_code: Optional[str]
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

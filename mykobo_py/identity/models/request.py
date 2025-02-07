from dataclasses import dataclass
from datetime import datetime

from dataclasses_json.api import dataclass_json

@dataclass_json
@dataclass
class CustomerRequest:
    id: str | None = None
    account: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email_address: str | None = None
    additional_name: str | None = None
    address: str | None = None
    mobile_number: str | None = None
    birth_date: str | None = None
    birth_country_code: str | None = None
    id_country_code: str | None = None
    bank_account_number: str | None = None
    tax_id: str | None = None
    tax_id_name: str | None = None
    credential_id: str | None = None

    @property
    def to_dict(self):
        return self.to_dict()

@dataclass_json
@dataclass
class UpdateProfileRequest:
    bank_account_number: str | None = None
    tax_id: str | None = None
    tax_id_name: str | None = None
    suspended_at: str | None = None
    deleted_at: str | None = None

    @property
    def to_dict(self):
        return self.to_dict()

@dataclass_json
@dataclass
class NewDocumentRequest:
    profile_id: str
    document_type: str
    document_status: str
    document_path: str | None = None
    created_at: str = datetime.now().isoformat()
    updated_at: str | None = None
    document_sub_type: str | None = None

    @property
    def to_dict(self):
        return self.to_dict()

@dataclass_json
@dataclass
class NewKycReviewRequest:
    profile_id: str
    level: str

    @property
    def to_dict(self):
        return self.to_dict()

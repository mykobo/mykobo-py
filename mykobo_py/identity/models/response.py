from typing import List, Optional, Dict
from datetime import datetime

from pydantic import BaseModel


class KycStatus(BaseModel):
    id: str
    profile_id: str
    review_status: str
    webhook_type: str
    applicant_id: str
    correlation_id: Optional[str] = None
    review_result: str
    received_at: datetime
    level_name: str
    admin_comment: Optional[str] = None
    user_comment: Optional[str] = None


class KycDocument(BaseModel):
    id: str
    profile_id: str
    document_type: str
    document_sub_type: Optional[str] = None
    document_status: str
    document_path: str
    reject_reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserProfile(BaseModel):
    id: str
    first_name: str
    last_name: str
    email_address: str
    additional_name: Optional[str] = None
    address: Optional[str] = None
    mobile_number: Optional[str] = None
    birth_date: Optional[datetime] = None
    birth_country_code: Optional[str] = None
    bank_account_number: Optional[str] = None
    tax_id: Optional[str] = None
    tax_id_name: Optional[str] = None
    created_at: datetime
    kyc_status: Optional[KycStatus] = None
    kyc_documents: List[KycDocument] = []


class ScoreIndicators(BaseModel):
    tax_residence_verified: float
    name_verified: float
    aml_passed: float
    phone_verified: float
    id_verified: float
    email_verified: float
    dob_verified: float
    residence_verified: float
    citizenship_verified: float
    is_not_pep: float


class Score(BaseModel):
    score: float
    breakdown: Dict[str, float]


class ScoreBreakdown(BaseModel):
    total_score: float
    verification: ScoreIndicators
    source_of_funds: Optional[Score] = None
    country_risk_jurisdiction: Optional[Score] = None
    expected_volume: Optional[Score] = None


class UserRiskProfile(BaseModel):
    risk_score: float
    latest_score_history: Optional[float] = None
    break_down: Optional[ScoreBreakdown] = None


class ProfileChangeLog(BaseModel):
    id: str
    profile_id: str
    changed_by_credential_id: str
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    created_at: datetime


class ProfileChangeLogResponse(BaseModel):
    profile_id: str
    total_changes: int
    logs: List[ProfileChangeLog] = []

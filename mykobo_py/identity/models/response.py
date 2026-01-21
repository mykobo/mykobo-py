from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class KycStatus:
    id: str
    profile_id: str
    review_status: str
    webhook_type: str
    applicant_id: str
    correlation_id: Optional[str]
    review_result: str
    received_at: datetime
    level_name: str
    admin_comment: Optional[str]
    user_comment: Optional[str]

    @staticmethod
    def from_json(json_payload: dict) -> 'KycStatus':
        return KycStatus(
            id=json_payload["id"],
            profile_id=json_payload["profile_id"],
            review_status=json_payload["review_status"],
            webhook_type=json_payload["webhook_type"],
            applicant_id=json_payload["applicant_id"],
            correlation_id=json_payload.get("correlation_id"),
            review_result=json_payload["review_result"],
            received_at=datetime.fromisoformat(json_payload["received_at"]),
            level_name=json_payload["level_name"],
            admin_comment=json_payload.get("admin_comment"),
            user_comment=json_payload.get("user_comment")
        )


@dataclass
class KycDocument:
    id: str
    profile_id: str
    document_type: str
    document_sub_type: Optional[str]
    document_status: str
    document_path: str
    reject_reason: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    @staticmethod
    def from_json(json_payload: dict) -> 'KycDocument':
        return KycDocument(
            id=json_payload["id"],
            profile_id=json_payload["profile_id"],
            document_type=json_payload["document_type"],
            document_sub_type=json_payload.get("document_sub_type"),
            document_status=json_payload["document_status"],
            document_path=json_payload["document_path"],
            reject_reason=json_payload.get("reject_reason"),
            created_at=datetime.fromisoformat(json_payload["created_at"]),
            updated_at=datetime.fromisoformat(json_payload["updated_at"]) if json_payload.get("updated_at") else None
        )


@dataclass
class UserProfile:
    id: str
    first_name: str
    last_name: str
    email_address: str
    additional_name: Optional[str]
    address: str
    mobile_number: str
    birth_date: Optional[datetime]
    birth_country_code: str
    bank_account_number: str
    tax_id: Optional[str]
    tax_id_name: Optional[str]
    created_at: datetime
    kyc_status: Optional[KycStatus]
    kyc_documents: List[KycDocument]

    @staticmethod
    def from_json(json_payload: dict) -> 'UserProfile':
        return UserProfile(
            id=json_payload["id"],
            first_name=json_payload["first_name"],
            last_name=json_payload["last_name"],
            email_address=json_payload["email_address"],
            additional_name=json_payload.get("additional_name"),
            address=json_payload["address"],
            mobile_number=json_payload["mobile_number"],
            birth_date=datetime.fromisoformat(json_payload["birth_date"]) if json_payload.get("birth_date") else None,
            birth_country_code=json_payload["birth_country_code"],
            bank_account_number=json_payload["bank_account_number"],
            tax_id=json_payload.get("tax_id"),
            tax_id_name=json_payload.get("tax_id_name"),
            created_at=datetime.fromisoformat(json_payload["created_at"]),
            kyc_status=KycStatus.from_json(json_payload["kyc_status"]) if json_payload.get("kyc_status") else None,
            kyc_documents=[KycDocument.from_json(doc) for doc in json_payload["kyc_documents"]]
        )

@dataclass
class ScoreIndicators:
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

    @staticmethod
    def from_json(json_payload: dict) -> 'ScoreIndicators':
        return ScoreIndicators(
            tax_residence_verified=json_payload["tax_residence_verified"],
            name_verified=json_payload["name_verified"],
            aml_passed=json_payload["aml_passed"],
            phone_verified=json_payload["phone_verified"],
            id_verified=json_payload["id_verified"],
            email_verified=json_payload["email_verified"],
            dob_verified=json_payload["dob_verified"],
            residence_verified=json_payload["residence_verified"],
            citizenship_verified=json_payload["citizenship_verified"],
            is_not_pep=json_payload["is_not_pep"]
        )

@dataclass
class Score:
    score: float
    breakdown: Dict[str, float]

    @staticmethod
    def from_json(json_payload: dict) -> 'Score':
        return Score(
            score=json_payload["score"],
            breakdown=json_payload["breakdown"]
        )

@dataclass
class ScoreBreakdown:
    total_score: float
    verification: ScoreIndicators
    source_of_funds: Score
    country_risk_jurisdiction: Optional[Score]
    expected_volume: Score

    @staticmethod
    def from_json(json_payload: dict) -> 'ScoreBreakdown':
        return ScoreBreakdown(
            total_score=json_payload["total_score"],
            verification=ScoreIndicators.from_json(json_payload["verification"]),
            source_of_funds=Score.from_json(json_payload["source_of_funds"]),
            country_risk_jurisdiction=Score.from_json(json_payload.get("country_risk_jurisdiction")),
            expected_volume=Score.from_json(json_payload["expected_volume"])
        )


@dataclass
class UserRiskProfile:
    risk_score: float
    latest_score_history: Optional[float]
    breakdown: ScoreBreakdown

    @staticmethod
    def from_json(json_payload: dict) -> 'UserRiskProfile':
        return UserRiskProfile(
            risk_score=json_payload["risk_score"],
            latest_score_history=json_payload.get("latest_score_history"),
            breakdown=ScoreBreakdown.from_json(json_payload.get("break_down"))
        )


@dataclass
class ProfileChangeLog:
    id: str
    profile_id: str
    changed_by_credential_id: str
    field_name: str
    old_value: Optional[str]
    new_value: Optional[str]
    created_at: datetime

    @staticmethod
    def from_json(json_payload: dict) -> 'ProfileChangeLog':
        return ProfileChangeLog(
            id=json_payload["id"],
            profile_id=json_payload["profile_id"],
            changed_by_credential_id=json_payload["changed_by_credential_id"],
            field_name=json_payload["field_name"],
            old_value=json_payload.get("old_value"),
            new_value=json_payload.get("new_value"),
            created_at=datetime.fromisoformat(json_payload["created_at"])
        )


@dataclass
class ProfileChangeLogResponse:
    profile_id: str
    total_changes: int
    logs: List[ProfileChangeLog]

    @staticmethod
    def from_json(json_payload: dict) -> 'ProfileChangeLogResponse':
        return ProfileChangeLogResponse(
            profile_id=json_payload["profile_id"],
            total_changes=json_payload["total_changes"],
            logs=[ProfileChangeLog.from_json(log) for log in json_payload["logs"]]
        )


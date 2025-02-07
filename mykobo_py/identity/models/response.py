from dataclasses import dataclass
from typing import List, Optional
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

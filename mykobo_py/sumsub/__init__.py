
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class AccessTokenRequest():
    # this is our profile id. For sumsub it would be external to them.
    external_user_id: str
    # level name is the KYC level for which to derive this token from. Usually the SEP6 level, if it's non-interactive
    level_name: str

    def to_dict(self) -> Dict:
        return {
            "externalUserId": self.external_user_id,
            "levelName": self.level_name
        }

@dataclass
class ProfileData():
    first_name: str
    last_name: str
    email: str

    def to_dict(self) -> Dict:
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email
        }


@dataclass
class NewApplicantRequest():
    external_user_id: str
    level_name: str
    profile: ProfileData

    @staticmethod
    def from_json(data: dict) -> 'NewApplicantRequest':
        return NewApplicantRequest(
            external_user_id=data.get('externalUserId', ''),
            level_name=data.get('levelName', ''),
            profile=ProfileData.from_json(data.get('profile', {}))
        )


@dataclass
class DocumentMetadata():
    id_doc_type: str
    id_doc_sub_type: Optional[str] = None
    country: Optional[str] = None

    @staticmethod
    def from_json(data: dict) -> 'DocumentMetadata':
        return DocumentMetadata(
            id_doc_type=data.get('idDocType', ''),
            id_doc_sub_type=data.get('idDocSubType'),
            country=data.get('country')
        )


@dataclass
class NewDocumentRequest():
    metadata: DocumentMetadata
    file_path: str
    applicant_id: str

    @staticmethod
    def from_json(data: dict) -> 'NewDocumentRequest':
        return NewDocumentRequest(
            metadata=DocumentMetadata.from_json(data.get('metadata', {})),
            file_path=data.get('file_path', ''),
            applicant_id=data.get('applicant_id', '')
        )


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

    def to_dict(self) -> Dict:
        return {
            "externalUserId": self.external_user_id,
            "levelName": self.level_name,
            "profile": self.profile.to_dict()
        }


@dataclass
class DocumentMetadata():
    id_doc_type: str
    id_doc_sub_type: Optional[str] = None
    country: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "idDocType": self.id_doc_type,
            "idDocSubType": self.id_doc_sub_type,
            "country": self.country
        }


@dataclass
class NewDocumentRequest():
    metadata: DocumentMetadata
    file_path: str
    applicant_id: str

    def to_dict(self) -> Dict:
        return {
            "metadata": self.metadata.to_dict(),
            "filePath": self.file_path,
            "applicantId": self.applicant_id
        }

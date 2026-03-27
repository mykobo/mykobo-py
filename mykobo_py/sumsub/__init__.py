
from typing import Optional, Dict

from pydantic import BaseModel, Field, ConfigDict


class AccessTokenRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # this is our profile id. For sumsub it would be external to them.
    external_user_id: str = Field(alias="externalUserId")
    # level name is the KYC level for which to derive this token from. Usually the SEP6 level, if it's non-interactive
    level_name: str = Field(alias="levelName")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class ProfileData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class NewApplicantRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    external_user_id: str = Field(alias="externalUserId")
    level_name: str = Field(alias="levelName")
    profile: ProfileData

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class DocumentMetadata(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_doc_type: str = Field(alias="idDocType")
    id_doc_sub_type: Optional[str] = Field(default=None, alias="idDocSubType")
    country: Optional[str] = None

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class NewDocumentRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    metadata: DocumentMetadata
    file_path: str = Field(alias="filePath")
    applicant_id: str = Field(alias="applicantId")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)

from typing import Dict, Optional

from pydantic import BaseModel, Field, ConfigDict


class AccessTokenRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    external_ref: str = Field(alias="externalRef")
    success_url: str = Field(alias="successUrl")
    error_url: str = Field(alias="errorUrl")
    unverified_url: str = Field(alias="unverifiedUrl")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class VerificationRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    external_ref: str = Field(alias="externalRef")
    first_name: Optional[str] = Field(default=None, alias="firstName")
    last_name: Optional[str] = Field(default=None, alias="lastName")
    date_of_birth: Optional[str] = Field(default=None, alias="dateOfBirth")
    sex: Optional[str] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    id_document_type: Optional[str] = Field(default=None, alias="idDocumentType")
    images: Optional[Dict[str, str]] = None
    # Session settings
    success_url: Optional[str] = Field(default=None, alias="successUrl")
    error_url: Optional[str] = Field(default=None, alias="errorUrl")
    unverified_url: Optional[str] = Field(default=None, alias="unverifiedUrl")
    callback_url: Optional[str] = Field(default=None, alias="callbackUrl")
    locale: Optional[str] = None
    expiry_time: Optional[int] = Field(default=None, alias="expiryTime")
    session_length: Optional[int] = Field(default=None, alias="sessionLength")
    token_type: Optional[str] = Field(default=None, alias="tokenType")
    show_instructions: Optional[bool] = Field(default=None, alias="showInstructions")
    generate_digit_string: Optional[bool] = Field(default=None, alias="generateDigitString")
    # Document data
    document_number: Optional[str] = Field(default=None, alias="documentNumber")
    personal_number: Optional[str] = Field(default=None, alias="personalNumber")
    date_of_expiry: Optional[str] = Field(default=None, alias="dateOfExpiry")
    date_of_issue: Optional[str] = Field(default=None, alias="dateOfIssue")
    # Verification features
    verify_email: Optional[bool] = Field(default=None, alias="verifyEmail")
    verify_phone: Optional[bool] = Field(default=None, alias="verifyPhone")
    verify_address: Optional[bool] = Field(default=None, alias="verifyAddress")
    nfc_required: Optional[bool] = Field(default=None, alias="nfcRequired")
    nfc_optional: Optional[bool] = Field(default=None, alias="nfcOptional")
    driver_license_back: Optional[bool] = Field(default=None, alias="driverLicenseBack")
    age_limit: Optional[int] = Field(default=None, alias="ageLimit")
    age_max: Optional[int] = Field(default=None, alias="ageMax")
    # Security checks
    check_liveness: Optional[bool] = Field(default=None, alias="checkLiveness")
    check_aml: Optional[bool] = Field(default=None, alias="checkAml")
    check_face_blacklist: Optional[bool] = Field(default=None, alias="checkFaceBlacklist")
    check_duplicate_faces: Optional[bool] = Field(default=None, alias="checkDuplicateFaces")
    check_duplicate_personal_data: Optional[bool] = Field(default=None, alias="checkDuplicatePersonalData")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)

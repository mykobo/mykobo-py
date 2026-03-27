from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class AccessTokenRequest:
    external_ref: str
    success_url: str
    error_url: str
    unverified_url: str

    def to_dict(self) -> Dict:
        return {
            "externalRef": self.external_ref,
            "successUrl": self.success_url,
            "errorUrl": self.error_url,
            "unverifiedUrl": self.unverified_url,
        }


@dataclass
class VerificationRequest:
    external_ref: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    sex: Optional[str] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    id_document_type: Optional[str] = None
    images: Optional[Dict[str, str]] = None
    # Session settings
    success_url: Optional[str] = None
    error_url: Optional[str] = None
    unverified_url: Optional[str] = None
    callback_url: Optional[str] = None
    locale: Optional[str] = None
    expiry_time: Optional[int] = None
    session_length: Optional[int] = None
    token_type: Optional[str] = None
    show_instructions: Optional[bool] = None
    generate_digit_string: Optional[bool] = None
    # Document data
    document_number: Optional[str] = None
    personal_number: Optional[str] = None
    date_of_expiry: Optional[str] = None
    date_of_issue: Optional[str] = None
    # Verification features
    verify_email: Optional[bool] = None
    verify_phone: Optional[bool] = None
    verify_address: Optional[bool] = None
    nfc_required: Optional[bool] = None
    nfc_optional: Optional[bool] = None
    driver_license_back: Optional[bool] = None
    age_limit: Optional[int] = None
    age_max: Optional[int] = None
    # Security checks
    check_liveness: Optional[bool] = None
    check_aml: Optional[bool] = None
    check_face_blacklist: Optional[bool] = None
    check_duplicate_faces: Optional[bool] = None
    check_duplicate_personal_data: Optional[bool] = None

    _FIELD_MAP = {
        "external_ref": "externalRef",
        "first_name": "firstName",
        "last_name": "lastName",
        "date_of_birth": "dateOfBirth",
        "id_document_type": "idDocumentType",
        "success_url": "successUrl",
        "error_url": "errorUrl",
        "unverified_url": "unverifiedUrl",
        "callback_url": "callbackUrl",
        "expiry_time": "expiryTime",
        "session_length": "sessionLength",
        "token_type": "tokenType",
        "show_instructions": "showInstructions",
        "generate_digit_string": "generateDigitString",
        "document_number": "documentNumber",
        "personal_number": "personalNumber",
        "date_of_expiry": "dateOfExpiry",
        "date_of_issue": "dateOfIssue",
        "verify_email": "verifyEmail",
        "verify_phone": "verifyPhone",
        "verify_address": "verifyAddress",
        "nfc_required": "nfcRequired",
        "nfc_optional": "nfcOptional",
        "driver_license_back": "driverLicenseBack",
        "age_limit": "ageLimit",
        "age_max": "ageMax",
        "check_liveness": "checkLiveness",
        "check_aml": "checkAml",
        "check_face_blacklist": "checkFaceBlacklist",
        "check_duplicate_faces": "checkDuplicateFaces",
        "check_duplicate_personal_data": "checkDuplicatePersonalData",
    }

    def to_dict(self) -> Dict:
        result = {}
        for py_field, json_field in self._FIELD_MAP.items():
            value = getattr(self, py_field)
            if value is not None:
                result[json_field] = value
        # Simple fields that don't need renaming
        for simple_field in ("sex", "nationality", "address", "country", "locale", "images"):
            value = getattr(self, simple_field)
            if value is not None:
                result[simple_field] = value
        return result

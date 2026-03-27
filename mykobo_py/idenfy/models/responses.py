from dataclasses import dataclass
from typing import Optional


@dataclass
class VerificationResponse:
    auth_token: str
    scan_ref: str
    client_id: str

    @staticmethod
    def from_dict(data: dict) -> "VerificationResponse":
        return VerificationResponse(
            auth_token=data["authToken"],
            scan_ref=data["scanRef"],
            client_id=data["clientId"],
        )


@dataclass
class VerificationPartialResponse:
    auth_token: str
    error: str
    data_status: str
    document_status: str

    @staticmethod
    def from_dict(data: dict) -> "VerificationPartialResponse":
        return VerificationPartialResponse(
            auth_token=data["authToken"],
            error=data["error"],
            data_status=data["dataStatus"],
            document_status=data["documentStatus"],
        )
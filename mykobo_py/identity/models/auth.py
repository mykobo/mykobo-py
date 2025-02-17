from dataclasses import dataclass
from datetime import datetime
import jwt

@dataclass
class Token:
    subject_id: str
    token: str
    refresh_token: str | None
    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        return datetime.now() >= self.expires_at

    @staticmethod
    def from_json(json_data: dict) -> 'Token':
        decoded = jwt.decode(json_data["token"], options={"verify_signature": False})
        return Token(
            subject_id=json_data["subject_id"],
            token=json_data["token"],
            refresh_token=json_data["refresh_token"],
            expires_at=datetime.fromtimestamp(decoded["exp"])
        )

    @staticmethod
    def from_jwt(jwt_token: str) -> 'Token':
        decoded = jwt.decode(jwt_token, options={"verify_signature": False})
        return Token(
            subject_id=decoded["sub"],
            token=jwt_token,
            refresh_token=None,
            expires_at=datetime.fromtimestamp(decoded["exp"])
        )

class OtcChallenge:
    def __init__(self, user_id: str, otp_required: bool, nonce: str):
        self.user_id = user_id
        self.otp_required = otp_required
        self.nonce = nonce

    @staticmethod
    def from_json(json_data: dict) -> 'OtcChallenge':
        return OtcChallenge(
            user_id=json_data["user_id"],
            otp_required=json_data["otp_required"],
            nonce=json_data["nonce"]
        )

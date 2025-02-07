from datetime import datetime
class ServiceToken:
    def __init__(self, subject_id: str, token: str, refresh_token: str, expires_at: datetime):
        self.subject_id = subject_id
        self.token = token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    @property
    def is_expired(self) -> bool:
        return datetime.now() >= self.expires_at

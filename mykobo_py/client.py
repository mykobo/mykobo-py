from logging import Logger
from typing import Optional

from mykobo_py.identity.models.auth import Token
class MykoboServiceClient:

    def __init__(self, logger: Logger, host: str):
        self.logger = logger
        self.host = host

    @staticmethod
    def generate_headers(token: Optional[Token], **kwargs) -> dict:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token.token}"
            headers["User-Agent"] = token.subject_id
        headers.update(kwargs)
        return headers

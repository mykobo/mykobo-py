from logging import Logger
from typing import Optional

from mykobo_py.identity.models.auth import ServiceToken
class MykoboServiceClient:

    def __init__(self, logger: Logger, host: str):
        self.logger = logger
        self.host = host

    def generate_headers(self, token: Optional[ServiceToken], **kwargs) -> dict:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token.token}"
            headers["User-Agent"] = token.subject_id
        headers.update(kwargs)
        return headers


from dataclasses import dataclass
from typing import Dict

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


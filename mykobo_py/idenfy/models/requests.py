
from dataclasses import dataclass
from typing import Dict

@dataclass
class AccessTokenRequest:
    external_ref: str
    success_url: str
    failure_url: str

    def to_dict(self) -> Dict:
        return {
            "externalRef": self.external_ref,
            "successUrl": self.success_url,
            "failureUrl": self.failure_url
        }


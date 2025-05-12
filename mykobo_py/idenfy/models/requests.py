
from dataclasses import dataclass
from typing import Dict

@dataclass
class AccessTokenRequest:
    # this is our profile id. For sumsub it would be external to them.
    profile_id: str

    def to_dict(self) -> Dict:
        return {
            "profile_id": self.profile_id
        }


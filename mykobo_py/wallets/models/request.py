from dataclasses import dataclass
from dataclasses_json.api import dataclass_json

@dataclass_json
@dataclass
class RegisterWalletRequest:
    profile_id: str
    public_key: str
    memo: str | None
    chain: str

    @property
    def to_dict(self):
        return self.to_dict()

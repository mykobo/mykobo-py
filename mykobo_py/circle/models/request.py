from dataclasses import dataclass
from typing import Optional

from dataclasses_json.api import dataclass_json


@dataclass_json
@dataclass
class CreateRelayAddressRequest:
    chain: str
    address: str
    private_key: str
    label: Optional[str] = None
    counterpart_id: Optional[str] = None
    external_address: Optional[str] = None
    client_domain: Optional[str] = None

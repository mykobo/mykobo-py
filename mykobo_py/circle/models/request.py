from dataclasses import dataclass
from typing import Optional

from dataclasses_json.api import dataclass_json


@dataclass_json
@dataclass
class RelayAddressSide:
    chain: str
    address: str
    private_key: str
    label: Optional[str] = None
    external_address: Optional[str] = None
    client_domain: Optional[str] = None
    email: Optional[str] = None


@dataclass_json
@dataclass
class CreateRelayAddressPairRequest:
    source: RelayAddressSide
    destination: RelayAddressSide

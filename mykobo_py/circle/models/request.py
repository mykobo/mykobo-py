from typing import Optional

from pydantic import BaseModel


class RelayAddressSide(BaseModel):
    chain: str
    address: str
    private_key: str
    label: Optional[str] = None
    external_address: Optional[str] = None
    client_domain: Optional[str] = None
    email: Optional[str] = None


class CreateRelayAddressPairRequest(BaseModel):
    source: RelayAddressSide
    destination: RelayAddressSide

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

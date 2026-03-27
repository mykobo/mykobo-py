from pydantic import BaseModel


class RegisterWalletRequest(BaseModel):
    profile_id: str
    public_key: str
    memo: str | None
    chain: str

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

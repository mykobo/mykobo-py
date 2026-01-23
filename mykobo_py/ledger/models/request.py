from dataclasses import dataclass
from typing import Dict, List, Optional
from mykobo_py.utils import del_none
from dataclasses_json.api import dataclass_json

@dataclass_json
@dataclass
class TransactionFilterRequest:
    sources: List[str]
    transaction_types: List[str]
    statuses: List[str]
    currencies: List[str]
    from_date: Optional[str]
    to_date: Optional[str]
    payee: Optional[str]
    payer:  Optional[str]
    page: int
    limit: int

    def to_dict(self) -> Dict:
        return del_none(self.to_dict())


@dataclass_json
@dataclass
class GetVerificationExceptionRequest:
    user_id: Optional[str]
    from_date: Optional[str]
    to_date: Optional[str]
    verifier_type: List[str]
    created_by: Optional[str]
    page: int
    limit: int

    def to_dict(self) -> Dict:
        return del_none(self.to_dict())

@dataclass_json
@dataclass
class AddVerificationException:
    user_id: str
    verifier_type: str
    error_code: str
    reason: str
    created_by: str
    expires_at: Optional[str]

    def to_dict(self) -> Dict:
        return del_none(self.to_dict())
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from dataclasses_json.api import dataclass_json

@dataclass_json
@dataclass
class FeeConfiguration:
    transaction_type: str
    fee_rate: float
    effective_from: str
    client_domain: str
    effective_until: Optional[str]
    created_by: str
    change_reason: str

from datetime import datetime


@dataclasses
@dataclasses_json
class FeeConfiguration:
    transaction_type: str
    fee_rate: float
    effective_from: datetime
    client_domain: str
    effective_until: datetime
    created_by: str
    change_reason: str

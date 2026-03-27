from typing import Optional

from pydantic import BaseModel


class Transaction(BaseModel):
    created_at: str = ''
    fee: str = '0'
    first_name: str = ''
    id: str = ''
    idempotency_key: str = ''
    incoming_currency: str = ''
    last_name: str = ''
    message_id: str = ''
    outgoing_currency: str = ''
    payee_id: Optional[str] = None
    payer_id: Optional[str] = None
    queue_sent_at: str = ''
    reference: str = ''
    source: str = ''
    status: str = ''
    transaction_type: str = ''
    tx_hash: Optional[str] = None
    updated_at: str = ''
    value: str = '0'
    wallet_address: str = ''
    network: Optional[str] = None
    client_domain: Optional[str] = None
    comment: Optional[str] = None

    @property
    def is_pending_anchor(self):
        return self.status == "PENDING_ANCHOR"

    @property
    def is_deposit(self):
        return self.transaction_type == "DEPOSIT"

    @property
    def is_withdrawal(self):
        return self.transaction_type == "WITHDRAWAL"

    @property
    def has_tx_hash(self):
        return self.tx_hash is not None and self.tx_hash != ""

    def dict(self, **kwargs) -> dict:
        d = self.model_dump()
        for key, value in d.items():
            if value is not None:
                d[key] = str(value)
        return d

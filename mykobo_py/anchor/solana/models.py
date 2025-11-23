from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Transaction:
    created_at: str
    fee: str
    first_name: str
    id: str
    idempotency_key: str
    incoming_currency: str
    last_name: str
    message_id: str
    outgoing_currency: str
    payee_id: Optional[str]
    payer_id: str
    queue_sent_at: str
    reference: str
    source: str
    status: str
    transaction_type: str
    tx_hash: Optional[str]
    updated_at: str
    value: str
    wallet_address: str

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

    @staticmethod
    def from_json(json_data: dict) -> 'Transaction':
        return Transaction(
            created_at=json_data.get('created_at', ''),
            fee=json_data.get('fee', '0'),
            first_name=json_data.get('first_name', ''),
            id=json_data.get('id', ''),
            idempotency_key=json_data.get('idempotency_key', ''),
            incoming_currency=json_data.get('incoming_currency', ''),
            last_name=json_data.get('last_name', ''),
            message_id=json_data.get('message_id', ''),
            outgoing_currency=json_data.get('outgoing_currency', ''),
            payee_id=json_data.get('payee_id'),
            payer_id=json_data.get('payer_id', ''),
            queue_sent_at=json_data.get('queue_sent_at', ''),
            reference=json_data.get('reference', ''),
            source=json_data.get('source', ''),
            status=json_data.get('status', ''),
            transaction_type=json_data.get('transaction_type', ''),
            tx_hash=json_data.get('tx_hash'),
            updated_at=json_data.get('updated_at', ''),
            value=json_data.get('value', '0'),
            wallet_address=json_data.get('wallet_address', '')
        )

    def dict(self):
        return {k: str(v) if v is not None else None for k, v in asdict(self).items()}

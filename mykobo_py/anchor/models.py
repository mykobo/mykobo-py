from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Amount:
    amount: str
    asset: str

    @staticmethod
    def from_json(json_data: dict) -> 'Amount':
        return Amount(
            amount=json_data.get('amount', '0'),
            asset=json_data.get('asset', '')
        )

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

@dataclass
class FeeDetail:
    name: str
    description: str
    amount: str

    @staticmethod
    def from_json(json_data: dict) -> 'FeeDetail':
        return FeeDetail(
            name=json_data.get('name', ''),
            description=json_data.get('description', ''),
            amount=json_data.get('amount', '')
        )

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

@dataclass
class FeeDetails:
    total: str
    asset: str
    details: List[FeeDetail]

    @staticmethod
    def from_json(json_data: dict) -> 'FeeDetails':
        return FeeDetails(
            total=json_data.get('total', '0'),
            asset=json_data.get('asset', ''),
            details=[FeeDetail.from_json(detail) for detail in json_data.get('details', [])]
        )

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

@dataclass
class Customer:
    account: str

    @staticmethod
    def from_json(json_data: dict) -> 'Customer':
        return Customer(
            account=json_data.get('account', '')
        )

    def to_dict(self) -> dict:
        return self.to_dict()

@dataclass
class Customers:
    sender: Customer
    receiver: Customer

    @staticmethod
    def from_json(json_data: dict) -> 'Customers':
        return Customers(
            sender=Customer.from_json(json_data.get('sender', {})),
            receiver=Customer.from_json(json_data.get('receiver', {}))
        )

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

@dataclass
class Creator:
    account: str

    @staticmethod
    def from_json(json_data: dict) -> 'Creator':
        return Creator(
            account=json_data.get('account', '')
        )

    def to_dict(self) -> dict:
        return self.to_dict()
@dataclass
class Transaction:
    fundingMethod: str
    id: str
    sep: str
    kind: str
    status: str
    type: str
    amount_expected: Amount
    amount_in: Amount
    amount_out: Amount
    fee_details: FeeDetails
    started_at: str
    updated_at: str
    message: str
    destination_account: str
    customers: Customers
    creator: Creator
    client_domain: str
    client_name: str

    @property
    def is_pending_payment(self):
        return self.status == "pending_user_transfer_start" and self.kind == "deposit"

    @staticmethod
    def from_json(json_data: dict) -> 'Transaction':
        return Transaction(
            fundingMethod=json_data.get('fundingMethod', ''),
            id=json_data.get('id', ''),
            sep=json_data.get('sep', ''),
            kind=json_data.get('kind', ''),
            status=json_data.get('status', ''),
            type=json_data.get('type', ''),
            amount_expected=Amount.from_json(json_data.get('amount_expected', {})),
            amount_in=Amount.from_json(json_data.get('amount_in', {})),
            amount_out=Amount.from_json(json_data.get('amount_out', {})),
            fee_details=FeeDetails.from_json(json_data.get('fee_details', {})),
            started_at=json_data.get('started_at', ''),
            updated_at=json_data.get('updated_at', ''),
            message=json_data.get('message', ''),
            destination_account=json_data.get('destination_account', ''),
            customers=Customers.from_json(json_data.get('customers', {})),
            creator=Creator.from_json(json_data.get('creator', {})),
            client_domain=json_data.get('client_domain', ''),
            client_name=json_data.get('client_name', '')
        )

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

from typing import List

from pydantic import BaseModel


class Amount(BaseModel):
    amount: str = '0'
    asset: str = ''


class FeeDetail(BaseModel):
    name: str = ''
    description: str = ''
    amount: str = ''


class FeeDetails(BaseModel):
    total: str = '0'
    asset: str = ''
    details: List[FeeDetail] = []


class Customer(BaseModel):
    account: str = ''


class Customers(BaseModel):
    sender: Customer = Customer()
    receiver: Customer = Customer()


class Creator(BaseModel):
    account: str = ''


class Transaction(BaseModel):
    fundingMethod: str = ''
    id: str = ''
    sep: str = ''
    kind: str = ''
    status: str = ''
    type: str = ''
    amount_expected: Amount = Amount()
    amount_in: Amount = Amount()
    amount_out: Amount = Amount()
    fee_details: FeeDetails = FeeDetails()
    started_at: str = ''
    updated_at: str = ''
    message: str = ''
    destination_account: str = ''
    customers: Customers = Customers()
    creator: Creator = Creator()
    client_domain: str = ''
    client_name: str = ''
    request_client_ip_address: str = ''

    @property
    def is_pending_off_chain_funds(self):
        return self.status == "pending_user_transfer_start" and self.kind == "deposit"

    @property
    def is_pending_on_chain_fulfillment(self):
        return self.status == "pending_anchor" and self.kind == "deposit"

    @property
    def is_pending_on_chain_funds(self):
        return self.status == "pending_user_transfer_start" and self.kind == "withdrawal"

    @property
    def is_pending_off_chain_fulfillment(self):
        return self.status == "pending_anchor" and self.kind == "withdrawal"

    @property
    def has_ip_address(self):
        return self.request_client_ip_address != ""

import os
from mykobo_py.client import MykoboServiceClient
from logging import Logger
import requests
from mykobo_py.identity.models.auth import Token
from mykobo_py.ledger.models.request import TransactionFilterRequest


class LedgerServiceClient(MykoboServiceClient):
    def __init__(self, host: str, logger: Logger):
        super().__init__(logger, host)
        self.app_key = os.getenv("IDENTLTY_ACCESS_KEY")
        self.app_secret = os.getenv("IDENTITY_SECRET_KEY")

    def transaction_list(self, token: Token, params: TransactionFilterRequest):
        """
        Get a list of transactions with a set of filter options

          {
              "sources": [],
              "transaction_types": [],
              "statuses":[],
              "currencies": [],
              "from":null, // datetime string
              "to": null, // datetime string iso formatted
              "payee":"urn:usrp:b26734fce23e450b87368b22cf56e091",
              "payer": "urn:usrp:b26734fce23e450b87368b22cf56e091",
              "page": 1,
              "limit": 2
           }
        """
        params_dict = params.to_dict()
        params_dict["from"] = params.from_date
        params_dict["to"] = params.to_date

        response = requests.post(
            f"{self.host}/transactions/list",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            json=params_dict
        )
        response.raise_for_status()
        return response.json()

    def get_transaction_statuses(self, token: Token):
        response = requests.get(
            f"{self.host}/transactions/statuses",
            headers=self.generate_headers(token, **{"Content-type": "application/json"})
        )
        response.raise_for_status()
        return response.json()

    def get_transaction_by_reference(self, token: Token, reference: str):
        response = requests.get(
            f"{self.host}/transactions/reference/{reference}/details",
            headers=self.generate_headers(token, **{"Content-type": "application/json"})
        )
        response.raise_for_status()
        return response.json()

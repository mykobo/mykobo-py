import json
import os
from typing import Optional
from mykobo_py.client import MykoboServiceClient
from logging import Logger
import requests
from mykobo_py.identity.models.auth import Token
from mykobo_py.ledger.models.request import TransactionFilterRequest, GetVerificationExceptionRequest, \
    AddVerificationException, RevokeExceptionRequest


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

        try:
            self.logger.info(f"Getting transactions with {params}")
            response = requests.post(
                f"{self.host}/transactions/list",
                headers=self.generate_headers(token, **{"Content-type": "application/json"}),
                json=params_dict
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.error(e)
            return {}

    def get_transaction_statuses(self, token: Token, status: Optional[str] = None):
        url = f"{self.host}/transactions/statuses"
        if status:
            url += f"/transitions/{status}"
        response = requests.get(
            url,
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

    def get_transaction_by_external_id(self, token: Token, external_id: str):
        response = requests.get(
            f"{self.host}/transactions/external/{external_id}",
            headers=self.generate_headers(token, **{"Content-type": "application/json"})
        )
        response.raise_for_status()
        return response.json()

    def get_transaction_compliance_events(self, token: Token, reference: str):
        response = requests.get(
            f"{self.host}/transactions/reference/{reference}/compliance",
            headers=self.generate_headers(token, **{"Content-type": "application/json"})
        )
        response.raise_for_status()
        return response.json()

    def get_transaction_stats(self, token: Token, to_date: Optional[str], from_date: Optional[str], profile_id: Optional[str]):
        url = f"{self.host}/transactions/stats"

        if to_date:
            url = f"{url}?to={to_date}"

        if from_date:
            if to_date:
                url = f"{url}&from={from_date}"
            else:
                url = f"{url}?from={from_date}"
        if profile_id:
            url = f"{url}&profile_id={profile_id}"

        response = requests.get(url, headers=self.generate_headers(token, **{"Content-type": "application/json"}))
        response.raise_for_status()
        return response.json()

    def get_compliance_gates(self, token: Token):
        url = f"{self.host}/transactions/compliance_gates"
        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"})
        )
        response.raise_for_status()
        return response.json()

    def get_verification_error_codes(self, token: Token):
        url = f"{self.host}/transactions/verification/error_codes"
        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"})
        )
        response.raise_for_status()
        return response.json()

    def get_exceptions(self, token: Token, params: GetVerificationExceptionRequest):
        params_dict = params.to_dict()
        params_dict["from"] = params.from_date
        params_dict["to"] = params.to_date

        url = f"{self.host}/transactions/exceptions"
        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            params=params_dict
        )
        response.raise_for_status()
        return response.json()

    def add_exception(self, token: Token, exception: AddVerificationException):
        url = f"{self.host}/transactions/exceptions"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            json=exception.to_dict()
        )
        response.raise_for_status()
        return response.json()

    def revoke_exception(self, token: Token, exception_id: int, exception: RevokeExceptionRequest):
        url = f"{self.host}/transactions/exceptions/{exception_id}/revoke"
        response = requests.put(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            json=exception.to_dict()
        )
        response.raise_for_status()
        return response.json()
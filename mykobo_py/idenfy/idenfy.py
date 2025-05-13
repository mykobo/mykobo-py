import json

import requests
from requests import Response

from mykobo_py.client import MykoboServiceClient
from mykobo_py.idenfy.models.requests import AccessTokenRequest


class IdenfyServiceClient(MykoboServiceClient):
    def __init__(self, host, logger):
        super().__init__(logger, host)


    def get_access_token(self, request: AccessTokenRequest) -> Response:
        """
        Get access token from Idenfy service, using parameters from AccessTokenRequest.
        """

        self.logger.info(f"Sending {request} to {self.host}...")
        url = f"{self.host}/access_token"
        response = requests.post(
            url,
            headers=self.generate_headers(None, **{"Content-type": "application/json"}),
            data=json.dumps(request.to_dict())
        )
        response.raise_for_status()
        return response

    def initiate_kyc(self, request: AccessTokenRequest):
        self.logger.info(f"Initiating KYC with {request} to {self.host}...")
        url = f"{self.host}/initiate_kyc"
        response = requests.post(
            url,
            headers=self.generate_headers(None, **{"Content-type": "application/json"}),
            data=json.dumps(request.to_dict())
        )
        response.raise_for_status()
        return response
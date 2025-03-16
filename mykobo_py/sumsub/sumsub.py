import requests
import json
from requests.models import Response
from mykobo_py.client import MykoboServiceClient
from mykobo_py.identity.models.auth import Token
from mykobo_py.sumsub.models.requests import AccessTokenRequest, NewApplicantRequest, NewDocumentRequest

class SumsubServiceClient(MykoboServiceClient):
    def __init__(self, host, logger):
        super().__init__(logger, host)

    def get_access_token(self, token: Token, request: AccessTokenRequest) -> Response:
        url = f"{self.host}/access_token"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(request.to_dict())
        )
        response.raise_for_status()
        return response

    def get_applicant(self, token: Token, profile_id: str) -> Response:
        url = f"{self.host}/get_applicant/{profile_id}"
        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def create_applicant(self, token: Token,  applicant_request: NewApplicantRequest) -> Response:
        url = f"{self.host}/create_applicant"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(applicant_request.to_dict())
        )
        response.raise_for_status()
        return response

    def submit_document(self, token: Token, new_document_request: NewDocumentRequest) -> Response:
        url = f"{self.host}/add_document"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(new_document_request.to_dict())
        )
        response.raise_for_status()
        return response

import json
import os
from datetime import datetime
from logging import Logger

import jwt
import requests
from requests import Response

from .models.auth import ServiceToken
from .models.request import CustomerRequest, NewDocumentRequest, NewKycReviewRequest
from mykobo_py.utils import del_none
from mykobo_py.client import MykoboServiceClient


class IdentityServiceClient(MykoboServiceClient):

    token: ServiceToken | None  = None
    def __init__(self, host: str, logger: Logger):
        super().__init__(logger, host)
        self.app_key = os.getenv("IDENTITY_ACCESS_KEY")
        self.app_secret = os.getenv("IDENTITY_SECRET_KEY")

    def acquire_token(self) -> ServiceToken | None:
        if self.token and not self.token.is_expired:
            return self.token

        try:
            data = data = dict(access_key=self.app_key, secret_key=self.app_secret)
            response = requests.post(
                f"{self.host}/authenticate",
                headers=self.generate_headers(None, **{"Content-type": "application/json"}),
                data=json.dumps(data)
            )
            if response.ok:
                json_response = response.json()
                decoded = jwt.decode(json_response["token"], options={"verify_signature": False})
                self.token = ServiceToken(
                    subject_id=json_response["subject_id"],
                    token=json_response["token"],
                    refresh_token=json_response["refresh_token"],
                    expires_at=datetime.fromtimestamp(decoded["exp"])
                )
                self.logger.info(f"Successfully acquired token from IDENTITY SERVICE for {self.token.subject_id}")
            else:
                try:
                    json_response = response.json()
                    if "error" in json_response:
                        self.logger.error(f"Failed to acquire token! Reason: {json_response['error']}")
                except Exception as e:
                    self.logger.error(f"Failed to acquire token! Reason: {response.content.decode('utf-8')}:{e}")
        except Exception as e:
            self.logger.warning("Could not acquire token. Reason: %s", e)
        return self.token


    def check_scope(self, target_token: str, scope: str) -> Response:
        response = requests.post(
            f"{self.host}/authorise/scope",
            data=json.dumps({"token": target_token, "scope": scope}),
            headers=self.generate_headers(self.acquire_token(), **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def check_subject(self, target_token: str, subject: str) -> Response:
        response = requests.post(
            f"{self.host}/authorise/subject",
            data=json.dumps({"token": target_token, "subject": subject}),
            headers=self.generate_headers(self.acquire_token(), **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def get_user_profile(self, id: str) -> Response:
        url = f"{self.host}/kyc/profile/{id}"
        self.logger.debug(f"Requesting user profile from IDENTITY SERVICE for {id}")
        response = requests.get(
            url, headers=self.generate_headers(self.acquire_token(), **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def create_new_customer(self, payload: CustomerRequest) -> Response:
        response = requests.post(
            f"{self.host}/user/profile/new",
            headers=self.generate_headers(self.acquire_token(), **{"Content-type": "application/json"}),
            data=json.dumps(del_none(payload.to_dict().copy()))
        )
        response.raise_for_status()
        return response

    def create_new_document(self, payload: NewDocumentRequest) -> Response:
        url = f"{self.host}/kyc/documents"
        response = requests.put(
            url,
            headers=self.generate_headers(self.acquire_token(), **{"Content-type": "application/json"}),
            data=json.dumps(del_none(payload.to_dict().copy()))
        )
        response.raise_for_status()
        return response


    def initiate_kyc_review(self, payload: NewKycReviewRequest) -> Response:
        url = f"{self.host}/kyc/reviews/initiate"
        response = requests.post(
            url,
            headers=self.generate_headers(self.acquire_token(), **{"Content-type": "application/json"}),
            data=json.dumps(del_none(payload.to_dict().copy()))
        )
        response.raise_for_status()
        return response

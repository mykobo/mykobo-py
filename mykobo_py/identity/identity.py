import json
import os
from typing import Optional

import requests
from logging import Logger
from requests import Response
from .models.auth import Token, OtcChallenge
from .models.request import CustomerRequest, NewDocumentRequest, NewKycReviewRequest, UpdateProfileRequest
from mykobo_py.utils import del_none
from mykobo_py.client import MykoboServiceClient
from mykobo_py.identity.models.request import UserProfileFilterRequest


class IdentityServiceClient(MykoboServiceClient):

    def __init__(self, host: str, logger: Logger):
        super().__init__(logger, host)
        self.app_key = os.getenv("IDENTITY_ACCESS_KEY")
        self.app_secret = os.getenv("IDENTITY_SECRET_KEY")


    def authenticate(self, email, password) -> Token | OtcChallenge:
        data = {
            "email": email,
            "password": password
        }

        response = requests.post(
            f"{self.host}/authenticate",
            headers=self.generate_headers(None, **{"Content-type": "application/json"}),
            data=json.dumps(data)
        )

        response.raise_for_status()

        if response.json().get("otp_required"):
            return OtcChallenge.from_json(response.json())
        else:
             return Token.from_json(response.json())

    def refresh_token(self, refresh_token: str) -> Token:
        data = {
            "refresh_token": refresh_token
        }

        response = requests.post(
            f"{self.host}/authenticate/refresh",
            headers=self.generate_headers(None, **{"Content-type": "application/json"}),
            data=json.dumps(data)
        )

        response.raise_for_status()
        return Token.from_json(response.json())


    def otp_challenge(self, nonce: str, otp: int) -> Token:
        data = {
            "nonce": nonce,
            "otp": otp
        }

        response = requests.post(
            f"{self.host}/authenticate/otp/validate",
            headers=self.generate_headers(None, **{"Content-type": "application/json"}),
            data=json.dumps(data)
        )

        response.raise_for_status()
        return Token.from_json(response.json())


    def acquire_token(self) -> Token | None:
        try:
            data = data = dict(access_key=self.app_key, secret_key=self.app_secret)
            response = requests.post(
                f"{self.host}/authenticate",
                headers=self.generate_headers(None, **{"Content-type": "application/json"}),
                data=json.dumps(data)
            )
            if response.ok:
                json_response = response.json()
                token = Token.from_json(json_response)
                self.logger.info(f"Successfully acquired token from IDENTITY SERVICE for {token.subject_id}")
                return token
            else:
                try:
                    json_response = response.json()
                    if "error" in json_response:
                        self.logger.error(f"Failed to acquire token! Reason: {json_response['error']}")
                        return None
                    return None
                except Exception as e:
                    self.logger.error(f"Failed to acquire token! Reason: {response.content.decode('utf-8')}:{e}")
                    return None
        except Exception as e:
            self.logger.warning("Could not acquire token. Reason: %s", e)
            return None

    def check_scope(self, token: Token, target_token: str, scope: str) -> Response:
        response = requests.post(
            f"{self.host}/authorise/scope",
            data=json.dumps({"token": target_token, "scope": scope}),
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def check_subject(self, token: Token, target_token: str, subject: str) -> Response:
        response = requests.post(
            f"{self.host}/authorise/subject",
            data=json.dumps({"token": target_token, "subject": subject}),
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def get_user_profile(self, token: Token, id: str) -> Response:
        url = f"{self.host}/user/profile/{id}"
        self.logger.debug(f"Requesting user profile from IDENTITY SERVICE for {id}")
        response = requests.get(
            url, headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def get_profile_with_token(self, token: Token) -> Response:
        url = f"{self.host}/user/profile"
        self.logger.debug(f"Requesting user profile from IDENTITY SERVICE for {token.subject_id} with token")
        response = requests.get(
            url, headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def get_user_kyc_profile(self, token: Token, id: str) -> Response:
        url = f"{self.host}/kyc/profile/{id}"
        self.logger.debug(f"Requesting user profile from IDENTITY SERVICE for {id}")
        response = requests.get(
            url, headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def create_new_customer(self,token: Token, payload: CustomerRequest) -> Response:
        response = requests.post(
            f"{self.host}/user/profile/new",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(del_none(payload.to_dict().copy()))
        )
        response.raise_for_status()
        return response

    def create_new_document(self, token: Token, payload: NewDocumentRequest) -> Response:
        url = f"{self.host}/kyc/documents"
        response = requests.put(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(del_none(payload.to_dict().copy()))
        )
        response.raise_for_status()
        return response


    def initiate_kyc_review(self, token: Token, payload: NewKycReviewRequest) -> Response:
        url = f"{self.host}/kyc/reviews/initiate"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(del_none(payload.to_dict().copy()))
        )
        response.raise_for_status()
        return response

    def list_profiles(self, token: Token, filters: UserProfileFilterRequest) -> Response:
        url = f"{self.host}/user/list"
        response = requests.post(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(del_none(filters.to_dict().copy()))
        )
        response.raise_for_status()
        return response


    def update_user_profile(self, token: Token, id: Optional[str], payload: UpdateProfileRequest) -> Response:
        url = f"{self.host}/user/profile/update"
        if id:
            url += f"/{id}"
        response = requests.patch(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(del_none(payload.to_dict().copy()))
        )
        response.raise_for_status()
        return response
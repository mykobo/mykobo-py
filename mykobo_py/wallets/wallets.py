from typing import Optional
import requests
from requests.models import Response

import json
from mykobo_py.client import MykoboServiceClient
from .models.request import RegisterWalletRequest
from mykobo_py.identity.models.auth import Token
from logging import Logger

class WalletServiceClient(MykoboServiceClient):
    def __init__(self, wallet_service_url: str, logger: Logger):
        super().__init__(logger, wallet_service_url)
        self.wallet_service_url = wallet_service_url

    def get_wallet_profile(self, token: Token, account: str, memo: Optional[str] = None) -> Response:
        url = f"{self.wallet_service_url}/user/wallet/{account}"
        if memo is not None:
            url += f"?memo={memo}"
        response = requests.get(
            url,
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

    def register_wallet(self, token: Token, request: RegisterWalletRequest) -> Response:
        response = requests.post(
            f"{self.wallet_service_url}/wallet/register",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
            data=json.dumps(request.to_dict())
        )
        response.raise_for_status()
        return response

    def get_user_wallets(self, token: Token, profile: str) -> Response:
        response = requests.get(
            f"{self.wallet_service_url}/wallet/user/{profile}",
            headers=self.generate_headers(token, **{"Content-type": "application/json"}),
        )
        response.raise_for_status()
        return response

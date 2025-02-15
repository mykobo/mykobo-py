import json
import logging
from dotenv import load_dotenv

from mykobo_py.identity.identity import IdentityServiceClient
from mykobo_py.identity.models.request import CustomerRequest
from os import getenv

from mykobo_py.identity.models.response import UserProfile
load_dotenv()
logger = logging.getLogger("test")
host = getenv("IDENTITY_SERVICE_HOST", "http://fallback")
identity_service = IdentityServiceClient(host, logger)

def test_service_authentication(requests_mock):
    with open("tests/stubs/authenticate_success.json") as f:
        json_data = json.loads(f.read())
        requests_mock.post(f"{host}/authenticate", json=json_data)
    token = identity_service.acquire_token()
    assert token
    assert token.subject_id == "urn:svc:94fc474ee7144ed181855d63f0a2bcad"
    assert token.token == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46c3ZjOjk0ZmM0NzRlZTcxNDRlZDE4MTg1NWQ2M2YwYTJiY2FkIiwianRpIjoidXJuOnRrbjoyZWU0N2ZjYTI2OTg0Y2MyODZjZDgyNDQ5NzVkNGVhYSIsImlzcyI6ImxvY2FsaG9zdCIsImlhdCI6MTczMjEyMDk4NCwiZXhwIjoxNzMyNzI1Nzg0LCJhdWQiOiJTZXJ2aWNlIiwic2NvcGUiOlsidXNlcjpyZWFkIiwidXNlcjp3cml0ZSIsInVzZXI6YWRtaW4iLCJzZXJ2aWNlOnJlYWQiLCJ0b2tlbjpyZWFkIiwiYnVzaW5lc3M6cmVhZCIsImJ1c2luZXNzOnJlYWQiLCJ3YWxsZXQ6cmVhZCIsIndhbGxldDp3cml0ZSIsInRyYW5zYWN0aW9uOnJlYWQiLCJ0cmFuc2FjdGlvbjp3cml0ZSIsInRyYW5zYWN0aW9uOmFkbWluIl19.t7Tl4kOf8emvPhUL4tTsBau9F3LEPFsnUAX7c2uxMVA"

def test_get_profile(requests_mock):
    id = "urn:usrp:fb497b2fcbfa479991de4e8b0abecad6"
    with open("tests/stubs/authenticate_success.json") as f:
        json_data = json.loads(f.read())
        requests_mock.post(f"{host}/authenticate", json=json_data)

    with open("tests/stubs/customer_kyc_complete.json") as f:
        json_data = json.loads(f.read())
        requests_mock.get(f"{host}/kyc/profile/{id}", json=json_data)

    profile = identity_service.get_user_profile(id)
    user_profile = UserProfile.from_json(profile.json())
    assert user_profile.id == "urn:usrp:fb497b2fcbfa479991de4e8b0abecad6"
    assert len(user_profile.kyc_documents) == 2
    assert user_profile.kyc_status
    assert user_profile.kyc_status.review_result == "GREEN"


def test_new_customer(requests_mock):
    with open("tests/stubs/authenticate_success.json") as f:
        json_data = json.loads(f.read())
        requests_mock.post(f"{host}/authenticate", json=json_data)

    with open("tests/stubs/new_customer.json") as f:
        json_data = json.loads(f.read())
        requests_mock.post(f"{host}/user/profile/new", json=json_data)


    payload = CustomerRequest(
        first_name="John",
        last_name="Doe",
        email_address="john@mykobo.co"
    )

    response = identity_service.create_new_customer(payload)
    print(response.json())
    assert response
    assert response.status_code == 200

    user_profile = UserProfile.from_json(response.json())
    assert user_profile.id == "urn:usrp:6dd61598f5be470ea19ca9b8ef012116"

import json

from mykobo_py.payment_intent.models import CreateReferenceRequest, ReferenceResponse


def test_create_reference_request_serialization():
    req = CreateReferenceRequest(
        profile_id="urn:usrp:test-user",
        wallet_address="GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
        client_domain="example.com",
    )
    data = req.model_dump()
    assert data["profile_id"] == "urn:usrp:test-user"
    assert data["wallet_address"] == "GABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
    assert data["client_domain"] == "example.com"


def test_create_reference_request_no_client_domain():
    req = CreateReferenceRequest(
        profile_id="urn:usrp:test-user",
        wallet_address="GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
    )
    data = req.model_dump()
    assert data["client_domain"] is None


def test_reference_response_deserialization():
    json_data = {
        "id": "urn:dpref:a1b2c3d4e5f6",
        "profile_id": "urn:usrp:test-user",
        "reference": "MYK-P-ABC12345",
        "is_active": True,
        "wallet_address": "GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
        "client_domain": "example.com",
        "created_at": "2026-06-13 12:00:00",
    }
    resp = ReferenceResponse(**json_data)
    assert resp.id == "urn:dpref:a1b2c3d4e5f6"
    assert resp.reference == "MYK-P-ABC12345"
    assert resp.is_active is True
    assert resp.wallet_address == "GABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
    assert resp.client_domain == "example.com"
    assert resp.created_at == "2026-06-13 12:00:00"


def test_reference_response_no_client_domain():
    json_data = {
        "id": "urn:dpref:a1b2c3d4e5f6",
        "profile_id": "urn:usrp:test-user",
        "reference": "MYK-P-ABC12345",
        "is_active": True,
        "wallet_address": "GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
        "created_at": "2026-06-13 12:00:00",
    }
    resp = ReferenceResponse(**json_data)
    assert resp.client_domain is None


def test_reference_response_list_deserialization():
    json_data = json.dumps([
        {
            "id": "urn:dpref:a1b2c3d4e5f6",
            "profile_id": "urn:usrp:test-user",
            "reference": "MYK-P-ABC12345",
            "is_active": True,
            "wallet_address": "GABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
            "created_at": "2026-06-13 12:00:00",
        },
        {
            "id": "urn:dpref:b2c3d4e5f6a1",
            "profile_id": "urn:usrp:test-user",
            "reference": "MYK-P-XYZ98765",
            "is_active": False,
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
            "client_domain": "other.example",
            "created_at": "2026-06-12 08:30:00",
        },
    ])
    data = json.loads(json_data)
    refs = [ReferenceResponse(**item) for item in data]
    assert len(refs) == 2
    assert refs[0].reference == "MYK-P-ABC12345"
    assert refs[0].is_active is True
    assert refs[1].reference == "MYK-P-XYZ98765"
    assert refs[1].is_active is False
    assert refs[1].client_domain == "other.example"

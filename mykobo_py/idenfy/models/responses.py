from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class VerificationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auth_token: str = Field(alias="authToken")
    scan_ref: str = Field(alias="scanRef")
    client_id: str = Field(alias="clientId")


class VerificationPartialResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auth_token: str = Field(alias="authToken")
    error: str
    data_status: str = Field(alias="dataStatus")
    document_status: str = Field(alias="documentStatus")

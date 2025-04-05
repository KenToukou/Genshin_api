from pydantic import UUID4

from .base_schema import BaseModel


class ClientCredentialsTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expire_in: int

    class Config:
        alias_generator = None
        schema_extra = {
            "example": {
                "access_token": "ACCESS_TOKEN",
                "token_type": "Bearer",
                "expire_in": 3600,
            }
        }


class UserInfo(BaseModel):
    id: UUID4
    name: str

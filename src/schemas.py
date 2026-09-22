import html
from typing import List
from pydantic import BaseModel, Field, field_validator, ConfigDict


def sanitize(value: str) -> str:
    """Экранирование HTML — защита от XSS."""
    return html.escape(value, quote=True)


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)

    @field_validator("username")
    @classmethod
    def clean_username(cls, v: str) -> str:
        return sanitize(v.strip())


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=5000)

    @field_validator("title", "content")
    @classmethod
    def clean_text(cls, v: str) -> str:
        return sanitize(v.strip())


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    author_id: int
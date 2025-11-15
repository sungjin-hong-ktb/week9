from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)
    model_config = ConfigDict(extra="forbid")

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        stripped = password.strip()
        if not stripped:
            raise ValueError("비밀번호를 입력해주세요.")
        return stripped

from __future__ import annotations

import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator

PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]).{8,20}$"
)

class UserBase(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=10)
    email: EmailStr
    model_config = ConfigDict(extra="forbid")

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, nickname: str) -> str:
        stripped = nickname.strip()
        if not stripped:
            raise ValueError("닉네임을 입력해주세요.")
        if " " in stripped:
            raise ValueError("띄어쓰기를 없애주세요.")
        return stripped

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=20)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not PASSWORD_PATTERN.match(password):
            raise ValueError(
                "비밀번호는 8~20자이며 대문자, 소문자, 숫자, 특수문자를 각각 최소 1개 포함해야 합니다."
            )
        return password


class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(default=None, min_length=1, max_length=10)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=20)
    model_config = ConfigDict(extra="forbid")

    @field_validator("nickname")
    @classmethod
    def validate_optional_nickname(cls, nickname: Optional[str]) -> Optional[str]:
        if nickname is None:
            return None
        stripped = nickname.strip()
        if not stripped:
            raise ValueError("닉네임을 입력해주세요.")
        if " " in stripped:
            raise ValueError("띄어쓰기를 없애주세요.")
        return stripped

    @field_validator("password")
    @classmethod
    def validate_optional_password(cls, password: Optional[str]) -> Optional[str]:
        if password is None:
            return None
        if not PASSWORD_PATTERN.match(password):
            raise ValueError(
                "비밀번호는 8~20자이며 대문자, 소문자, 숫자, 특수문자를 각각 최소 1개 포함해야 합니다."
            )
        return password


class UserResponse(BaseModel):
    id: int
    nickname: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

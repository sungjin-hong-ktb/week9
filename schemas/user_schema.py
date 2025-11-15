import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]).{8,20}$"
)

class UserCreate(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=10)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("닉네임을 입력해주세요.")
        if len(trimmed) > 10:
            raise ValueError("닉네임은 최대 10자 까지 작성 가능합니다.")
        if " " in trimmed:
            raise ValueError("띄어쓰기를 없애주세요.")
        return trimmed

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not PASSWORD_PATTERN.match(value):
            raise ValueError("비밀번호는 8~20자이며 대문자, 소문자, 숫자, 특수문자를 각각 최소 1개 포함해야 합니다.")
        return value

class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=1, max_length=10)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=20)

    @field_validator("nickname")
    @classmethod
    def validate_optional_nickname(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("닉네임을 입력해주세요.")
        if len(trimmed) > 10:
            raise ValueError("닉네임은 최대 10자 까지 작성 가능합니다.")
        if " " in trimmed:
            raise ValueError("띄어쓰기를 없애주세요.")
        return trimmed

    @field_validator("password")
    @classmethod
    def validate_optional_password(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not PASSWORD_PATTERN.match(value):
            raise ValueError("비밀번호는 8~20자이며 대문자, 소문자, 숫자, 특수문자를 각각 최소 1개 포함해야 합니다.")
        return value

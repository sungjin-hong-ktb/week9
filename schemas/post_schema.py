from typing import Optional

from pydantic import BaseModel, Field, field_validator

class PostCreate(BaseModel):
    title: str = Field(..., max_length=26)
    content: str
    author_id: int
    author_name: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("제목을 입력해주세요.")
        if len(trimmed) > 26:
            raise ValueError("제목은 26자 이내로 작성해주세요.")
        return trimmed

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("내용을 입력해주세요.")
        return trimmed

    @field_validator("author_name")
    @classmethod
    def validate_author_name(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("작성자 이름을 입력해주세요.")
        return trimmed

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=26)
    content: Optional[str] = None
    author_id: Optional[int] = None
    author_name: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_optional_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("제목을 입력해주세요.")
        if len(trimmed) > 26:
            raise ValueError("제목은 26자 이내로 작성해주세요.")
        return trimmed

    @field_validator("content")
    @classmethod
    def validate_optional_content(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("내용을 입력해주세요.")
        return trimmed

    @field_validator("author_name")
    @classmethod
    def validate_optional_author_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("작성자 이름을 입력해주세요.")
        return trimmed

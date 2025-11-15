from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class PostBase(BaseModel):
    title: str = Field(..., max_length=26)
    content: str
    author_id: int
    author_name: str
    model_config = ConfigDict(extra="forbid")

    @field_validator("title")
    @classmethod
    def validate_title(cls, title: str) -> str:
        stripped = title.strip()
        if not stripped:
            raise ValueError("제목을 입력해주세요.")
        if len(stripped) > 26:
            raise ValueError("제목은 26자 이내로 작성해주세요.")
        return stripped

    @field_validator("content")
    @classmethod
    def validate_content(cls, content: str) -> str:
        stripped = content.strip()
        if not stripped:
            raise ValueError("내용을 입력해주세요.")
        return stripped

    @field_validator("author_name")
    @classmethod
    def validate_author_name(cls, author_name: str) -> str:
        stripped = author_name.strip()
        if not stripped:
            raise ValueError("작성자 이름을 입력해주세요.")
        return stripped


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=26)
    content: Optional[str] = None
    author_id: Optional[int] = None
    author_name: Optional[str] = None
    model_config = ConfigDict(extra="forbid")

    @field_validator("title")
    @classmethod
    def validate_optional_title(cls, title: Optional[str]) -> Optional[str]:
        if title is None:
            return None
        stripped = title.strip()
        if not stripped:
            raise ValueError("제목을 입력해주세요.")
        if len(stripped) > 26:
            raise ValueError("제목은 26자 이내로 작성해주세요.")
        return stripped

    @field_validator("content")
    @classmethod
    def validate_optional_content(cls, content: Optional[str]) -> Optional[str]:
        if content is None:
            return None
        stripped = content.strip()
        if not stripped:
            raise ValueError("내용을 입력해주세요.")
        return stripped

    @field_validator("author_name")
    @classmethod
    def validate_optional_author_name(cls, author_name: Optional[str]) -> Optional[str]:
        if author_name is None:
            return None
        stripped = author_name.strip()
        if not stripped:
            raise ValueError("작성자 이름을 입력해주세요.")
        return stripped


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    author_name: str
    created_at: datetime
    updated_at: datetime
    views: int
    likes: int
    model_config = ConfigDict(from_attributes=True)

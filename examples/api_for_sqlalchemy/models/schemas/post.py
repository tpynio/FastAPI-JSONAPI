"""Post base schemas module."""

from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_rest_jsonapi.schema_base import BaseModel, Field, RelationshipInfo

if TYPE_CHECKING:
    from .user import UserSchema


class PostBaseSchema(BaseModel):
    """Post base schema."""

    class Config:
        """Pydantic schema config."""

        orm_mode = True

    title: str
    body: str


class PostPatchSchema(PostBaseSchema):
    """Post PATCH schema."""


class PostInSchema(PostBaseSchema):
    """Post input schema."""


class PostSchema(PostInSchema):
    """Post item schema."""

    class Config:
        """Pydantic model config."""

        orm_mode = True

    id: int
    created_at: datetime = Field(description="Create datetime")
    modified_at: datetime = Field(description="Update datetime")

    user: "UserSchema" = Field(
        relationship=RelationshipInfo(
            resource_type="user",
        ),
    )

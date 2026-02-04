"""Pydantic models for the Albums API."""

from __future__ import annotations

from pydantic import AnyUrl, BaseModel, ConfigDict, Field


class AlbumBase(BaseModel):
    """Common album fields."""

    title: str = Field(min_length=1, max_length=200)
    artist: str = Field(min_length=1, max_length=200)
    price: float = Field(ge=0.0)
    image_url: AnyUrl


class AlbumCreate(AlbumBase):
    """Request body for creating an album."""


class AlbumUpdate(BaseModel):
    """Request body for updating an album (partial update)."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    artist: str | None = Field(default=None, min_length=1, max_length=200)
    price: float | None = Field(default=None, ge=0.0)
    image_url: AnyUrl | None = None


class Album(AlbumBase):
    """Album returned by the API."""

    id: int = Field(ge=1)

    model_config = ConfigDict(from_attributes=True)

"""FastAPI app for the Albums API."""

from __future__ import annotations

import logging
import os
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from albums_api.models import Album, AlbumCreate, AlbumUpdate
from albums_api.repository import AlbumNotFoundError, InMemoryAlbumRepository

logger = logging.getLogger(__name__)


def _configure_logging() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


_configure_logging()

app = FastAPI(
    title="Albums API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

_repo = InMemoryAlbumRepository()


@app.get("/", response_class=PlainTextResponse)
def root() -> str:
    """Health/info endpoint."""

    return "Hit the /albums endpoint to retrieve a list of albums!"


@app.get("/albums", response_model=list[Album])
def list_albums() -> list[Album]:
    """Return all albums."""

    return _repo.list_albums()


@app.get("/albums/{album_id}", response_model=Album)
def get_album(album_id: Annotated[int, Path(ge=1)]) -> Album:
    """Return a single album by id."""

    try:
        return _repo.get_album(album_id)
    except AlbumNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Album {album_id} not found",
        ) from exc


@app.post("/albums", response_model=Album, status_code=status.HTTP_201_CREATED)
def create_album(payload: AlbumCreate) -> Album:
    """Create a new album."""

    album = _repo.create_album(payload)
    logger.info("Created album id=%s", album.id)
    return album


@app.put("/albums/{album_id}", response_model=Album)
def update_album(
    album_id: Annotated[int, Path(ge=1)],
    payload: AlbumUpdate,
) -> Album:
    """Update an existing album (partial update)."""

    try:
        album = _repo.update_album(album_id, payload)
    except AlbumNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Album {album_id} not found",
        ) from exc

    logger.info("Updated album id=%s", album.id)
    return album


@app.delete("/albums/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(album_id: Annotated[int, Path(ge=1)]) -> Response:
    """Delete an album."""

    try:
        _repo.delete_album(album_id)
    except AlbumNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Album {album_id} not found",
        ) from exc

    logger.info("Deleted album id=%s", album_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_default_port() -> int:
    """Return the default port for the service.

    The original .NET sample runs on port 3000.
    """

    try:
        return int(os.getenv("PORT", "3000"))
    except ValueError:
        return 3000

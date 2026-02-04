"""In-memory storage for albums.

The service is intentionally database-free to match the sample app behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock

from albums_api.models import Album, AlbumCreate, AlbumUpdate


@dataclass(frozen=True, slots=True)
class _SeedAlbum:
    id: int
    title: str
    artist: str
    price: float
    image_url: str


_SEED_ALBUMS: list[_SeedAlbum] = [
    _SeedAlbum(
        1,
        "You, Me and an App Id",
        "Daprize",
        10.99,
        "https://aka.ms/albums-daprlogo",
    ),
    _SeedAlbum(
        2,
        "Seven Revision Army",
        "The Blue-Green Stripes",
        13.99,
        "https://aka.ms/albums-containerappslogo",
    ),
    _SeedAlbum(
        3,
        "Scale It Up",
        "KEDA Club",
        13.99,
        "https://aka.ms/albums-kedalogo",
    ),
    _SeedAlbum(
        4,
        "Lost in Translation",
        "MegaDNS",
        12.99,
        "https://aka.ms/albums-envoylogo",
    ),
    _SeedAlbum(
        5,
        "Lock Down Your Love",
        "V is for VNET",
        12.99,
        "https://aka.ms/albums-vnetlogo",
    ),
    _SeedAlbum(
        6,
        "Sweet Container O' Mine",
        "Guns N Probeses",
        14.99,
        "https://aka.ms/albums-containerappslogo",
    ),
]


class AlbumNotFoundError(KeyError):
    """Raised when an album cannot be found."""


class InMemoryAlbumRepository:
    """Thread-safe in-memory album repository."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._albums: dict[int, Album] = {
            seed.id: Album(
                id=seed.id,
                title=seed.title,
                artist=seed.artist,
                price=seed.price,
                image_url=seed.image_url,
            )
            for seed in _SEED_ALBUMS
        }

    def list_albums(self) -> list[Album]:
        """Return all albums, sorted by id."""

        with self._lock:
            return [self._albums[key] for key in sorted(self._albums)]

    def get_album(self, album_id: int) -> Album:
        """Return a single album.

        Raises:
            AlbumNotFoundError: If the album does not exist.
        """

        with self._lock:
            try:
                return self._albums[album_id]
            except KeyError as exc:
                raise AlbumNotFoundError(album_id) from exc

    def create_album(self, payload: AlbumCreate) -> Album:
        """Create and return a new album."""

        with self._lock:
            next_id = (max(self._albums) + 1) if self._albums else 1
            album = Album(id=next_id, **payload.model_dump())
            self._albums[next_id] = album
            return album

    def update_album(self, album_id: int, payload: AlbumUpdate) -> Album:
        """Update an existing album and return it.

        Raises:
            AlbumNotFoundError: If the album does not exist.
        """

        with self._lock:
            if album_id not in self._albums:
                raise AlbumNotFoundError(album_id)

            current = self._albums[album_id]
            update_data = payload.model_dump(exclude_unset=True)
            updated = current.model_copy(update=update_data)
            self._albums[album_id] = updated
            return updated

    def delete_album(self, album_id: int) -> None:
        """Delete an album.

        Raises:
            AlbumNotFoundError: If the album does not exist.
        """

        with self._lock:
            try:
                del self._albums[album_id]
            except KeyError as exc:
                raise AlbumNotFoundError(album_id) from exc

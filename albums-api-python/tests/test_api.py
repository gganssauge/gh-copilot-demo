"""API tests for the Albums API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from albums_api.app import app


def test_root_returns_message() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "Hit the /albums endpoint" in response.text


def test_list_albums_returns_seed_data() -> None:
    client = TestClient(app)

    response = client.get("/albums")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 6
    assert data[0]["id"] == 1
    assert data[0]["image_url"].startswith("https://")


def test_get_album_returns_album() -> None:
    client = TestClient(app)

    response = client.get("/albums/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_album_missing_returns_404() -> None:
    client = TestClient(app)

    response = client.get("/albums/9999")

    assert response.status_code == 404


def test_create_update_delete_album_round_trip() -> None:
    client = TestClient(app)

    create = client.post(
        "/albums",
        json={
            "title": "My Album",
            "artist": "Me",
            "price": 1.25,
            "image_url": "https://example.com/cover.png",
        },
    )
    assert create.status_code == 201
    created = create.json()
    album_id = created["id"]

    update = client.put(
        f"/albums/{album_id}",
        json={
            "price": 2.50,
        },
    )
    assert update.status_code == 200
    assert update.json()["price"] == 2.50

    delete = client.delete(f"/albums/{album_id}")
    assert delete.status_code == 204

    missing = client.get(f"/albums/{album_id}")
    assert missing.status_code == 404

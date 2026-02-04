# Albums API (Python)

FastAPI reimplementation of the `albums-api` service.

## Prerequisites

- `uv` installed (https://docs.astral.sh/uv/)

## Setup

From this folder:

- Install dependencies (including dev tools): `uv sync --all-extras`

## Run (dev)

- `uv run uvicorn albums_api.app:app --reload --host 0.0.0.0 --port 3000`

Then open:

- http://localhost:3000/ (root message)
- http://localhost:3000/albums (albums list)
- http://localhost:3000/docs (Swagger UI)

## Test

- `uv run pytest`

## Lint

- `uv run ruff check .`

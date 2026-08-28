# Acme Orders

A minimal FastAPI service used as the sample application for **Release Commander**.

## Endpoints

- `GET /health` — health check, returns `{"status": "ok"}`
- `GET /orders` — list orders
- `POST /orders` — create an order

## Quickstart

```bash
uvicorn main:app --reload
```

## Run tests

```bash
pip install -e ".[dev]"
pytest
```

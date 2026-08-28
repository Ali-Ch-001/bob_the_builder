from fastapi import FastAPI

from app.models import Order

app = FastAPI(title="Acme Orders")

_next_id = 1


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/orders")
def get_orders() -> list[Order]:
    return []


@app.post("/orders")
def create_order(order: Order) -> Order:
    global _next_id
    order.id = _next_id
    _next_id += 1
    return order

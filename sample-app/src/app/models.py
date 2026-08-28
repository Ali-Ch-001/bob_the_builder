from pydantic import BaseModel


class Order(BaseModel):
    id: int
    customer: str
    items: list[str] | int
    total: float

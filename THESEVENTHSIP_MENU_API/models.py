from pydantic import BaseModel


class SingleMenuItem(BaseModel):
    id: int
    name: str
    category: str
    price: float
    description: str
    available: bool


class MultiMenuItems(BaseModel):
    status: str = "success"
    count: int
    items: list[SingleMenuItem]

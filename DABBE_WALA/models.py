from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

# what is enum?
# An enum is a symbolic name for a set of values.
# It is a data type that consists of a set of named values called elements or members.
# In programming, enums are used to represent a collection of related constants, making the code more readable and maintainable.


# OrderStatus (Enum) -> preparing, picked_up, on_the_way, delivered
class OrderStatus(str, Enum):
    PREPARING = "preparing"
    PICKED_UP = "picked_up"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"


# db schema
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    delivery_address: str
    items: str
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# schema for creating new order
class CreateOrder(SQLModel):
    customer_name: str
    items: str
    delivery_address: str


# schema for updating an order status
class UpdateOrder(SQLModel):
    status: Optional[OrderStatus] = None
    delivery_address: Optional[str] = None


class StatusLOG(SQLModel):
    order_id: int
    old_status: str
    new_status: str
    changed_at: datetime

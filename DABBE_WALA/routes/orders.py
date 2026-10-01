from fastapi import APIRouter, Depends, Query, HTTPException
from database import get_session
from models import Order, CreateOrder, OrderStatus, UpdateOrder
from sqlmodel import Session, select
from datetime import datetime, timezone

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order)
def create_order(order: CreateOrder, session: Session = Depends(get_session)):
    order_db = Order.model_validate(order)
    session.add(order_db)
    session.commit()
    session.refresh(order_db)

    return order_db


@router.get("/", response_model=list[Order])
def list_orders(
    status: OrderStatus | None = Query(
        default=None, description="Filter by order status"),
    created_date: str | None = Query(
        default=None, description="Filter by creation date (YYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    query = select(Order)

    if status:
        query = query.where(Order.status == status)

    if created_date:
        start = datetime.combine(
            created_date, datetime.min.time(), tzinfo=timezone.utc)
        end = datetime.combine(
            created_date, datetime.max.time(), tzinfo=timezone.utc)

        query = query.where(Order.created_at >= start, Order.created_at <= end)

    query = query.offset(skip).limit(limit)

    return session.exec(query).all()


@router.patch("/{order_id}", response_model=Order)
def update_order(
    order_id: int,
    order_update: UpdateOrder,
    session: Session = Depends(get_session)
):
    # Find the order by id
    order = session.get(Order, order_id)

    # If order doesn't exist
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Update status if provided
    if order_update.status is not None:
        order.status = order_update.status

    # Update delivery address if provided
    if order_update.delivery_address is not None:
        order.delivery_address = order_update.delivery_address

    # Update timestamp
    order.updated_at = datetime.now(timezone.utc)

    session.add(order)
    session.commit()
    session.refresh(order)

    return order

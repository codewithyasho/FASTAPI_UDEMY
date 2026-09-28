from datetime import datetime, date, timezone
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from models import Order, OrderStatus
from database import get_session
from zoneinfo import ZoneInfo


router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/daily")
def daily_summary(
    summary_date: date | None = Query(
        default=None,
        description="Date for the summary (YYYY-MM-DD)"
    ),
    session: Session = Depends(get_session)
):
    if summary_date is None:
        summary_date = date.today()

    india_tz = ZoneInfo("Asia/Kolkata")

    # Start of the day in India
    start_ist = datetime.combine(
        summary_date,
        datetime.min.time(),
        tzinfo=india_tz
    )

    # End of the day in India
    end_ist = datetime.combine(
        summary_date,
        datetime.max.time(),
        tzinfo=india_tz
    )

    # Convert India time → UTC for database query
    start = start_ist.astimezone(timezone.utc)
    end = end_ist.astimezone(timezone.utc)

    summary = {}
    total = 0

    for status in OrderStatus:
        count = session.exec(
            select(func.count(Order.id)).where(
                Order.created_at >= start,
                Order.created_at <= end,
                Order.status == status
            )
        ).one()

        summary[status.value] = count
        total += count

    return {
        "date": summary_date.isoformat(),
        "summary": summary,
        "total_orders": total,
    }

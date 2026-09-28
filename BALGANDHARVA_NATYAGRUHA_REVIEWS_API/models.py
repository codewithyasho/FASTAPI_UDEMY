from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from uuid import uuid4


# this is only database schema not validation
class Review(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True
    )
    play_name: str = Field(index=True)
    reviewer_name: str
    rating: float = Field(ge=1, le=5)
    comment: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# validations:
# create
class CreateReview(SQLModel):
    play_name: str
    reviewer_name: str
    rating: float = Field(ge=1, le=5)
    comment: str


# read
class ReadReview(SQLModel):
    id: str
    play_name: str
    reviewer_name: str
    rating: float
    comment: str
    created_at: datetime


# update
class UpdateReview(SQLModel):
    rating: Optional[float] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func
from models import Review, CreateReview, ReadReview, UpdateReview
from database import get_session

# Group all routes in this file under the "/review/" URL prefix and label them for documentation
router = APIRouter(prefix="/review", tags=["reviews"])


# This endpoint CREATES and SAVES a single new review sent by a user
@router.post("/", response_model=ReadReview)
def create_review(review: CreateReview, session: Session = Depends(get_session)):
    # 1. Convert the incoming user data into an official SQLModel database row item
    db_review = Review(**review.model_dump())

    # 2. Place the new review item into Python's temporary database "shopping cart"
    session.add(db_review)

    # 3. Press the "checkout" button to permanently write and save it into the database file
    session.commit()

    # 4. Refresh the item to pull in database-generated data (like its new unique ID)
    session.refresh(db_review)

    # 5. Return the newly created review back to the user to confirm it was successfully saved
    return db_review


# this endpoint will list the reviews with filter and pagination
@router.get("/", response_model=list[ReadReview])
def list_review(
    playname: str | None = Query(
        default=None, description="filter by playname"),
    # offset
    skip: int = Query(0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(10, ge=1, le=50, description="Max reviews to return"),
    session: Session = Depends(get_session)
):
    # sqlmodel way of writing the SQL queries
    query = select(Review)

    if playname:
        query = query.where(Review.play_name == playname)

    query = query.offset(skip).limit(limit)

    reviews = session.exec(query).all()

    return reviews


# endpoint for dispalying the avg of the ratings for a particular play
@router.get("/average/{playname}")
def get_avg_rating(playname: str, session: Session = Depends(get_session)):

    # sqlmodel way of writing the SQL queries
    result = session.exec(
        select(func.avg(Review.rating), func.count(Review.id)).where(
            Review.play_name == playname
        )
    ).first()

    avg_rating, total_reviews_count = result

    verdict = "People Dislike it." if avg_rating < 3.0 else "People are Loving it."

    if total_reviews_count == 0:
        raise HTTPException(
            status_code=404, detail=f"No review found for: {playname}")

    return {
        "play_name": playname,
        "total_reviews": total_reviews_count,
        "average_rating": avg_rating,
        "final_verdict": verdict
    }


@router.get("/{review_id}", response_model=ReadReview)
def get_review_by_id(review_id: str, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)

    if not review:
        raise HTTPException(
            status_code=404, detail=f"NO review found of id: {review_id}")

    return review


@router.patch("/{review_id}", response_model=ReadReview)
def update_review_by_id(review_id: str, update: UpdateReview, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)

    if not review:
        raise HTTPException(
            status_code=404, detail=f"NO review found of id: {review_id}")

    update_data = update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(review, key, value)

    session.add(review)
    session.commit()
    session.refresh(review)

    return review


@router.delete("/{review_id}")
def delete_review_by_id(review_id: str, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)

    if not review:
        raise HTTPException(
            status_code=404, detail=f"NO review found of id: {review_id}")

    session.delete(review)
    session.commit()

    return {
        "message": "Review Deleted."
    }


# TODO: endpoint for top 3 plays.

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func
from models import Review, CreateReview, ReadReview, UpdateReview
from database import get_session

# Group all routes in this file under the "/review/" URL prefix and label them for documentation
router = APIRouter(prefix="/review", tags=["reviews"])


# ENDPOINT 1: this endpoint will list all the plays with its reviews.
@router.get("/list", response_model=list[ReadReview], description="List all the plays with its reviews")
def list_reviews(session: Session = Depends(get_session)):
    # sqlmodel way of writing the SQL queries
    query = select(Review)

    reviews = session.exec(query).all()

    return reviews


# ENDPOINT 2: this endpoint will list all the unique plays only.
@router.get("/list/plays", response_model=list[str], description="List all the unique plays")
def list_plays(session: Session = Depends(get_session)):
    # sqlmodel way of writing the SQL queries
    query = select(Review.play_name).distinct()

    plays = session.exec(query).all()

    return plays


# ENDPOINT 3: this endpoint will list all the reviews with filter and pagination of a particular play.
@router.get(
    "/filter",
    response_model=list[ReadReview],
    description="List all the reviews of a particular play with filter and pagination"
)
def filter_reviews(
    playname: str | None = Query(
        default=None, description="filter by playname"),
    # offset
    skip: int = Query(0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(10, ge=1, le=50, description="Max reviews to return"),
    session: Session = Depends(get_session)
):

    if not playname:
        raise HTTPException(
            status_code=400, detail="Please provide a playname to filter reviews.")

    query = select(Review)

    query = query.where(Review.play_name == playname)

    query = query.offset(skip).limit(limit)

    reviews = session.exec(query).all()

    return reviews


# ENDPOINT 4: This endpoint CREATE, SAVE and DISPLAYS a single new review sent by a user
@router.post("/create", response_model=ReadReview, description="Create a new review for a play")
def create_review(review: CreateReview, session: Session = Depends(get_session)):

    db_review = Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


# ENDPOINT 5: this endpoint displays the top 3 plays with its reviews.
@router.get("/top3", response_model=list[ReadReview], description="List the top 3 plays")
def get_top3_plays(session: Session = Depends(get_session)):
    query = select(Review).order_by(Review.rating.desc()).limit(3)

    top3_reviews = session.exec(query).all()

    return top3_reviews


# ENDPOINT 6: this is the endpoint for dispalying the avg of the ratings for a particular play.
@router.get("/average/{playname}", description="Get the average rating for a particular play")
def get_avg_rating(playname: str, session: Session = Depends(get_session)):

    # sqlmodel way of writing the SQL queries
    result = session.exec(
        select(func.avg(Review.rating), func.count(Review.id)).where(
            Review.play_name == playname
        )
    ).first()

    avg_rating, total_reviews_count = result

    verdict = "People Dislike it." if avg_rating < 3 else "People are Loving it."

    if total_reviews_count == 0:
        raise HTTPException(
            status_code=404, detail=f"No review found for: {playname}")

    return {
        "play_name": playname,
        "total_reviews": total_reviews_count,
        "average_rating": round(avg_rating, 2),
        "final_verdict": verdict
    }


# ENDPOINT 7: Get all reviews by play name
@router.get("/play/{play_name}", response_model=list[ReadReview])
def get_reviews_by_play(
    play_name: str,
    session: Session = Depends(get_session)
):
    statement = select(Review).where(Review.play_name == play_name)

    reviews = session.exec(statement).all()

    if not reviews:
        raise HTTPException(
            status_code=404,
            detail=f"No reviews found for play: {play_name}"
        )

    return reviews


# ENDPOINT 8: Update a review by its ID
@router.patch("/update/{review_id}", response_model=ReadReview)
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


# EndPOINT 9: Delete a review by its ID
@router.delete("/delete/{review_id}")
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


# ENDPOINT 10: Get the most frequent reviewer

@router.get(
    "/top-reviewer",
    description="Get the reviewer who has submitted the most reviews"
)
def get_most_frequent_reviewer(
    session: Session = Depends(get_session)
):
    query = (
        select(
            Review.reviewer_name,
            func.count(Review.id).label("review_count")
        )
        .group_by(Review.reviewer_name)
        .order_by(func.count(Review.id).desc())
        .limit(1)
    )

    result = session.exec(query).first()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No reviews found."
        )

    reviewer_name, review_count = result

    return {
        "reviewer_name": reviewer_name,
        "review_count": review_count
    }

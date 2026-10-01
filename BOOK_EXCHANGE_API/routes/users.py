from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from database import get_session
from models.user import User, ReadUser, CreateUser
from auth import verify_api_key


router = APIRouter(prefix="/users", tags=["Users"])


# endpoint for creating a new user
@router.post("/", response_model=ReadUser)
def create_user(
    user_data: CreateUser,
    session: Session = Depends(get_session),
    x_api_key: str = Depends(verify_api_key)
):

    # matching the api key with the env
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User.model_validate(user_data)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


# endpont for listing all users
@router.get("/", response_model=list[ReadUser])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


# ALWAYS REMEMBER:
'''
POST → creating a NEW DB object
       ↓
       model_validate()

PATCH → updating an EXISTING DB object
       ↓
       model_dump(exclude_unset=True)
       ↓
       update only sent fields
'''

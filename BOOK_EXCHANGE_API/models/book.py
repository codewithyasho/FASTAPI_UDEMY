from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: float
    is_sold: bool = Field(default=False)

    # foreign key to user table
    user_id: int = Field(foreign_key="user.id")
    # one book can have one owner
    owner: Optional["User"] = Relationship(back_populates="books")


# request body model for creating a new book
class CreateBook(SQLModel):
    title: str
    author: str
    price: float
    user_id: int


# response body model for read book
class ReadBook(SQLModel):
    id: int
    title: str
    author: str
    price: float
    is_sold: bool
    user_id: int


# update book model for updating a book
class UpdateBook(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    is_sold: Optional[bool] = None


# avoiding circular import by importing Book at the end of the file
from models.user import User
Book.model_rebuild()

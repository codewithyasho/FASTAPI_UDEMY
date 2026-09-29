from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


# db schema for user table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str

    # one user can have many books
    books: list["Book"] = Relationship(back_populates="owner")


# request body model for creating a new user
class CreateUser(SQLModel):
    name: str
    email: str
    college: str


# response body model for read user
class ReadUser(SQLModel):
    id: int
    name: str
    email: str
    college: str


# avoiding circular import by importing Book at the end of the file
from models.book import Book
User.model_rebuild()  # Rebuild the model to resolve forward references

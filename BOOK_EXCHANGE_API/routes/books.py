from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from database import get_session
from models.book import Book, ReadBook, CreateBook, UpdateBook
from auth import verify_api_key
from typing import Optional


router = APIRouter(prefix="/books", tags=["Books"])


# endpoint for listing all books
@router.get("/", response_model=list[ReadBook])
def list_books(
    title: Optional[str] = Query(
        default=None, description="Enter book title to filter"),
    author: Optional[str] = Query(
        default=None, description="Enter book author to filter"),
    session: Session = Depends(get_session)
):
    query = select(Book).where(
        Book.is_sold == False
    )

    if title:
        query = query.where(Book.title.contains(title))

    if author:
        query = query.where(Book.author.contains(author))

    books = session.exec(query).all()
    return books


# endpoint for creating a new book
@router.post("/", response_model=ReadBook)
def create_book(
    book_data: CreateBook,
    api_key: str = Depends(verify_api_key),
    session: Session = Depends(get_session),
):

    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    new_book = Book.model_validate(book_data)

    session.add(new_book)
    session.commit()
    session.refresh(new_book)

    return new_book


# endpoint for updating a book
@router.patch("/{book_id}", response_model=ReadBook)
def update_book(
    book_id: int,
    update_book_data: UpdateBook,
    api_key: str = Depends(verify_api_key),
    session: Session = Depends(get_session),
):
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    get_book = session.get(Book, book_id)

    if not get_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # here not using model_validate because we are not creating a new Book object.
    #
    book_data = update_book_data.model_dump(exclude_unset=True)

    for key, value in book_data.items():
        setattr(get_book, key, value)

    session.add(get_book)
    session.commit()
    session.refresh(get_book)

    return get_book


# endpoint for marking a book as sold
@router.patch("/{book_id}/sold", response_model=ReadBook)
def mark_book_as_sold(
    book_id: int,
    api_key: str = Depends(verify_api_key),
    session: Session = Depends(get_session),
):
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    get_book = session.get(Book, book_id)
    if not get_book:
        raise HTTPException(status_code=404, detail="Book not found")

    get_book.is_sold = True
    session.add(get_book)
    session.commit()
    session.refresh(get_book)

    return get_book


# endpoint for deleting a book
@router.delete("/{book_id}", response_model=ReadBook)
def delete_book(
    book_id: int,
    api_key: str = Depends(verify_api_key),
    session: Session = Depends(get_session),
):
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    get_book = session.get(Book, book_id)
    if not get_book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(get_book)
    session.commit()

    return get_book


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


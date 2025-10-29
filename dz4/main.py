import logging
from collections.abc import Callable
from enum import StrEnum, auto
from typing import ParamSpec, Self, TypeVar

from pydantic import BaseModel, EmailStr

R = TypeVar("R")
P = ParamSpec("P")

logger = logging.getLogger(__name__)


def log_operation(fn: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info(f"{fn}: {args}, {kwargs}")
        return fn(*args, **kwargs)

    return wrapper


class BookCategories(StrEnum):
    FICTION = auto()
    FANTASY = auto()
    MYSTERY = auto()
    ROMANCE = auto()


class Book(BaseModel):
    title: str
    author: str
    year: int
    available: bool
    categories: list[BookCategories]


class User(BaseModel):
    name: str
    email: EmailStr
    membership_id: str


class Library:
    books: list[Book]
    users: list[User]

    def total_books(self: Self) -> int:
        return len(self.books)


class BookNotAvailable(Exception):
    def __init__(self: Self, book: Book) -> None:
        self.book = book

    def __str__(self: Self) -> str:
        return f"Book not available: {self.book}"


@log_operation
def add_book(books: list[Book], book: Book) -> None:
    books.append(book)


@log_operation
def find_book(books: list[Book], title: str) -> Book | None:
    for book in books:
        if book.title == title:
            return book


@log_operation
def is_book_borrow(book: Book) -> bool:
    if not book.available:
        raise BookNotAvailable(book)
    return True


@log_operation
def return_book(book: Book) -> None:
    book.available = True

"""
This file is a part of fastapi where
we are using pydantic for data validation while
using POST method to insert new data.
Here we are not going to use Body to send data
but we will use pydantic.
"""
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:

    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id, title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date

# this class is used to validate the post parameter values
class BookRequest(BaseModel):
    # id: Optional[int] = None # here making id optional to pass as a parameter
    id: int = Field(description="ID is not required", default=None)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0 , lt=6)
    publish_date: int = Field(gt=1999 , lt=2031)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "meetboghani",
                "description": "A new book description",
                "rating": 5,
                "publish_date": 2000,
            }
        }
    }

Books = [
    Book(1, "title one", "author 1", "description 1", 5, 2012),
    Book(2, "title two", "author 2", "description 2", 1, 2011),
    Book(3, "title three", "author 3", "description 3", 3, 2011),
    Book(4, "title four", "author 4", "description 4", 4, 2020),
    Book(5, "title five", "author 5", "description 5", 5, 2021)
]

@app.get("/books/publish_date", status_code=status.HTTP_200_OK)
async def read_book(publish_date: int = Query(gt=1999 , lt=2031)): # Query used to validate the input
    book_list = []
    for book in Books:
        if book.publish_date == publish_date:
            book_list.append(book)

    return book_list

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_books():
    return Books

@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookRequest):
    new_book = Book(**book.dict())
    Books.append(increment_id(new_book))

def increment_id(book: Book):
    book.id = 1 if len(Books) == 0 else Books[-1].id + 1
    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_books(book: BookRequest):
    book_changed = False
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = book
            book_changed = True

    if not book_changed: raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int = Path(gt=0)): #Path used to validate the input passing in the url
    book_changed = False
    for i in range(len(Books)):
        if Books[i].id == id:
            Books.pop(i)
            book_changed = True
            break

    if not book_changed: raise HTTPException(status_code=404, detail="Item not found.")

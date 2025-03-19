from array import array

from fastapi import FastAPI, Body

app = FastAPI()

Books =[
    {'Title': 'Title One', "author" : "author one", 'category': 'science'},
    {'Title': 'Title two', "author" : "author one", 'category': 'history'},
    {'Title': 'Title three', "author" : "author two", 'category': 'maths'},
    {'Title': 'Title four', "author" : "author three", 'category': 'ss'},
    {'Title': 'Title six', "author" : "author four", 'category': 'science'},
]
@app.get("/books")
async def books():
    return Books

# fastapi using dynamic path parameter
@app.get("/books/{book_title}") #passing book title as dynamic parameter
async def book(book_title: str):
    for book in Books:
        if book['Title'].casefold() == book_title.casefold(): return book

# fastapi using dynamic path parameter and query paramter
@app.get("/books/{author}/") #passing book title as dynamic parameter
async def book(author: str, category: str):
    book_list = []
    for book in Books:
        if book['author'].casefold() == author.casefold() and book["category"].casefold() == category.casefold():
           book_list.append(book)

    return book_list

# FASTAPI function with post method
@app.post("/books/send_data")
async def add_new_book(new_book = Body()):
    Books.append(new_book)

# FASTAPI function with put method
@app.put("/books/update_data")
async def add_new_book(update_book = Body()):
    for i in range(len(Books)):
        if Books[i]["Title"].casefold() == update_book["Title"].casefold():
            Books[i] = update_book

# FASTAPI function with delete method
@app.delete("/books/delete_book/{book_title}")
async def add_new_book(book_title: str):
    # for book in Books:
    #     if book["Title"].casefold() == book_title.casefold():
    #         Books.remove(book)
    #         break
    for i in range(len(Books)):
        if Books[i]["Title"].casefold() == book_title.casefold():
            Books.pop(i)
            break

# Assignment to fetch all books using author parameter
@app.get("/books/by_author/{book_author}") #passing book author as dynamic parameter
async def author_data(book_author: str):
    book_list = []
    for book in Books:
        if book.get('author').casefold() == book_author.casefold():
            book_list.append(book)

    return book_list
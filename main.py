from fastapi import FastAPI, HTTPException
from classes import Item, Book
from utils import mongo_serialize

app = FastAPI()

import pymongo
from bson.objectid import ObjectId
from mysecret import MONGODBSTR
mongo_client = pymongo.MongoClient(MONGODBSTR)
print(mongo_client)
db = mongo_client.book_library
coll_books = db['books']

items = []

# ROUTES
@app.get('/')
def root():
    return {'hello':'world'}

@app.post('/items')
def create_item(item: Item):
    items.append(item)
    return items

@app.get('/items', response_model=list[Item])
def list_items(limit:int = 10):
    return items[0:limit]

@app.get('/items/{item_id}', response_model=Item)
def get_item(item_id: int) -> Item:
    try:
        item = items[item_id]
        return item
    except:
        raise HTTPException(status_code=404, detail=f'Item {item_id} not found')

# BOOK ROUTES
@app.get('/books')
def list_books():
    "List all books"
    r = [mongo_serialize(book) for book in coll_books.find()]
    print(r)
    if r:
        return r
    else:
        return HTTPException(status_code=204, detail=f'No items')
    
@app.get('/books/{book_id}')
def get_book(book_id:str):
    filter = {'_id': ObjectId(book_id)}
    r = coll_books.find_one(filter)
    print('look for', filter)
    print(r)
    if r:
        return mongo_serialize(r)
    else:
        return HTTPException(status_code=204, detail=f'No items')
    
@app.post('/books')
def add_book(book: Book) -> str:
    """ insert a book
    """
    print(book)
    r = coll_books.insert_one(dict(book))
    
    return f"created ObjectId('{r.inserted_id}')"

# PUT to change whole book

# patch to change details of the book
@app.patch('/books')
def edit_book():
    pass

# lease?
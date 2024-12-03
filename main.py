from fastapi import FastAPI, HTTPException
from classes import Item, Book, UpdateBook
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

# @app.post('/items')
# def create_item(item: Item):
#     items.append(item)
#     return items

# @app.get('/items', response_model=list[Item])
# def list_items(limit:int = 10):
#     return items[0:limit]

# @app.get('/items/{item_id}', response_model=Item)
# def get_item(item_id: int) -> Item:
#     try:
#         item = items[item_id]
#         return item
#     except:
#         raise HTTPException(status_code=404, detail=f'Item {item_id} not found')

# BOOK ROUTES
@app.get('/books')
def list_books(
    name: str | None = None, 
    author: str | None = None, 
    year: int | None = None):
    """List all books"""
    filter = {}
    if name:
        filter['name'] = {'$regex':name, '$options':'i'} 
    if author:
        filter['author'] = {'$regex':author, '$options':'i'} 
    if year:
        filter['year'] = year
    r = [mongo_serialize(book) for book in coll_books.find(filter)]
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



# patch to change details of the book
@app.patch('/books/{book_id}')
def edit_book(book_id: str, book: UpdateBook):
    try:
        filter = {'_id': ObjectId(book_id)}
        r = coll_books.find_one(filter)
    except:
        return {"error": "Not valid Id"}
    
    if r:
        print(dict(book.model_dump(exclude_unset=True)))
        updated_result = coll_books.update_one(
            filter,
            {"$set":dict(book.model_dump(exclude_unset=True))}
        )
        return {'message':f'matched: {updated_result.matched_count}, updated: {updated_result.modified_count}'} 
        
    else:
        return {"error": "Item not found"}

@app.patch('/books/')    
def edit_book_many(ids: list[str], books: list[UpdateBook]):        
    resp = []
    for i in range(len(ids)):
        resp.append(edit_book(ids[i], books[i]))
    return resp


    

def find_and_operate(operation_func):
    def inner1(book_id: str):

        try:
            filter = {'_id': ObjectId(book_id)}
            r = coll_books.find_one(filter)
        except:
            return {"error": "Not valid Id"}
        
        if r:
            return operation_func(book_id, filter)
            
        else:
            return {"error": "Item not found"}
    return inner1



# DELETE BOOK
@app.delete('/books/{book_id}')
@find_and_operate
def delete_book(book_id: str, *args):
    filter = args[0]
    print(book_id)
    r = coll_books.delete_one(filter)
    return {'message':f'successfully deleted: {r.deleted_count}'} 


# lease?

# PUT to change whole book
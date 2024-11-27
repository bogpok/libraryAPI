from fastapi import FastAPI, HTTPException
from classes import Item
import pymongo

from mysecret import MONGODBSTR

app = FastAPI()
mongo_client = pymongo.MongoClient(MONGODBSTR)
print(mongo_client)




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


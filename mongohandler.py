# from mysecret import MONGODBSTR
# import pymongo
# mongo_client = pymongo.MongoClient(MONGODBSTR)
# print(mongo_client)
# db = mongo_client.book_library
# coll_books = db['books']


# def get_books():
#     r = list(coll_books.find())
#     print(r)
#     # if r:
#     #     return r
#     # else:
#     #     HTTPException(status_code=204, detail=f'No items')

# get_books()



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://customAtlasUser:qwerty2281337@myatlasclusteredu.rpqdz.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# HELP
"""
https://github.com/mongodb-university/atlas_starter_python/blob/master/atlas-starter.py
"""
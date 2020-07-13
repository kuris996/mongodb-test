import asyncio
from motor import motor_asyncio as ma
from bson.objectid import ObjectId

MONGODB_HOST = 'mongodb://user:1@127.0.0.1:27017/test'
MONGODB_NAME = 'test'
MY_COLLECTION = "my"

class MyModel:
    def __init__(self, db):
        self.db = db
        self.collection = db[MY_COLLECTION]

    async def save(self, name):
        result = await self.collection.insert_one({
            'name' : name,
        })
        return result

    async def load(self, id):
        result = await self.collection.find_one({
            '_id' : id
        })
        return result

async def init():
    client = ma.AsyncIOMotorClient(MONGODB_HOST)
    db = client[MONGODB_NAME]
    return client, db

loop = asyncio.get_event_loop()
client, db = loop.run_until_complete(init())
my_model = MyModel(db)
result = loop.run_until_complete(my_model.save("test"))
loaded = loop.run_until_complete(my_model.load(result.inserted_id))
print(loaded.get('name'))
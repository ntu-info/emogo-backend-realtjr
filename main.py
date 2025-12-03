from fastapi import FastAPI
from pydantic import BaseModel
import motor.motor_asyncio

app = FastAPI()

# -------------------------
# MongoDB 連線設定
# -------------------------
MONGODB_URI = "mongodb+srv://anna23qq_db_user:NztrnGfV8ay2UJlv@cluster0.gfssdel.mongodb.net/"
DB_NAME = "emogo_db"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

# -------------------------
# Pydantic Model
# -------------------------
class Item(BaseModel):
    name: str
    value: int

# -------------------------
# Routes
# -------------------------

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI + MongoDB!"}


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    result = await db["items"].insert_one(item_dict)
    return {"inserted_id": str(result.inserted_id)}


@app.get("/items")
async def get_items():
    items = []
    cursor = db["items"].find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        items.append(document)
    return items


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

from fastapi import FastAPI
from pydantic import BaseModel
import motor.motor_asyncio
import os

app = FastAPI()

# -------------------------
# MongoDB Connection
# -------------------------
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "emogo_db"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

# -------------------------
# Emogo Data Model
# -------------------------
class EmogoRecord(BaseModel):
    emotion: str
    location: dict
    timestamp: int
    video: str   # webm filename

# -------------------------
# Routes
# -------------------------

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI + Emogo!"}

# 1. Insert Emogo Data
@app.post("/records")
async def create_record(record: EmogoRecord):
    result = await db["records"].insert_one(record.dict())
    return {"inserted_id": str(result.inserted_id)}

# 2. Get All Records
@app.get("/records")
async def get_records():
    records = []
    cursor = db["records"].find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        records.append(doc)
    return records

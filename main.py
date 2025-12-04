from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

# 2. Get All Records (JSON)
@app.get("/records")
async def get_records():
    records = []
    cursor = db["records"].find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        records.append(doc)
    return records

# 3. Dashboard Page (HTML)
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    # Fetch records
    records = []
    cursor = db["records"].find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        records.append(doc)

    # HTML Template
    html = """
    <html>
    <head>
        <title>EmoGo Dashboard</title>
        <style>
            table { border-collapse: collapse; width: 90%; margin: 20px auto; }
            th, td { border: 1px solid #666; padding: 8px; text-align: left; }
            th { background-color: #eee; }
            h1 { text-align: center; }
        </style>
    </head>
    <body>
        <h1>EmoGo Dashboard</h1>
        <table>
            <tr>
                <th>Emotion</th>
                <th>Timestamp</th>
                <th>Latitude</th>
                <th>Longitude</th>
                <th>Video Filename</th>
            </tr>
    """

    for r in records:
        html += f"""
        <tr>
            <td>{r.get('emotion')}</td>
            <td>{r.get('timestamp')}</td>
            <td>{r.get('location', {}).get('lat')}</td>
            <td>{r.get('location', {}).get('lon')}</td>
            <td>{r.get('video')}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return HTMLResponse(content=html)

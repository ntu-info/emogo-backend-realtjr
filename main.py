from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import motor.motor_asyncio
import os
import json

app = FastAPI()

# -------------------------
# MongoDB Connection
# -------------------------
MONGODB_URI = os.getenv("MONGO_URI")  # make sure Render uses this name
DB_NAME = "emogo_db"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

# -------------------------
# Static folder for videos
# -------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------
# Emogo Data Model
# -------------------------
class EmogoRecord(BaseModel):
    emotion: str
    location: dict
    timestamp: int
    video: str   # webm filename only


@app.get("/")
async def root():
    return {"message": "Emogo Backend is Running!"}


# -------------------------
# Insert Records
# -------------------------
@app.post("/records")
async def create_record(record: EmogoRecord):
    result = await db["records"].insert_one(record.dict())
    return {"inserted_id": str(result.inserted_id)}


# -------------------------
# Get All Records (JSON)
# -------------------------
@app.get("/records")
async def get_records():
    records = []
    cursor = db["records"].find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        records.append(doc)
    return records


# -------------------------
# Download JSON File
# -------------------------
@app.get("/download/json")
async def download_json():
    records = []
    cursor = db["records"].find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        records.append(doc)

    json_data = json.dumps(records, indent=4)

    headers = {
        "Content-Disposition": "attachment; filename=emogo_records.json"
    }

    return Response(content=json_data, media_type="application/json", headers=headers)


# -------------------------
# Download Video File
# -------------------------
@app.get("/download/video/{filename}")
async def download_video(filename: str):
    filepath = f"static/videos/{filename}"
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="video/webm", filename=filename)
    return {"error": "File not found", "path": filepath}


# -------------------------
# Dashboard Page (HTML)
# -------------------------
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    # pull records
    records = []
    cursor = db["records"].find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        records.append(doc)

    # build HTML table
    rows = ""
    for r in records:
        rows += f"""
        <tr>
            <td>{r['_id']}</td>
            <td>{r['emotion']}</td>
            <td>{r['location']}</td>
            <td>{r['timestamp']}</td>
            <td>
                <a href="/download/video/{r['video']}" target="_blank">
                    {r['video']}
                </a>
            </td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>Emogo Dashboard</title>
        <style>
            body {{
                font-family: Arial;
                margin: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .download-btn {{
                padding: 10px 14px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 6px;
            }}
        </style>
    </head>

    <body>
        <h1>Emogo Dashboard</h1>

        <a class="download-btn" href="/download/json">Download All JSON</a>

        <table>
            <tr>
                <th>ID</th>
                <th>Emotion</th>
                <th>Location</th>
                <th>Timestamp</th>
                <th>Video</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    return HTMLResponse(content=html)

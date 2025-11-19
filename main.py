import os
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import (
    Moodentry,
    Worry,
    Assessmentresult,
    Crisisplan,
    Thoughtchallenge,
    Meditationsession,
    Habit,
    Habitlog,
    Recovery,
    Recoverylog,
    Garden,
    Reflection,
    Usersettings,
    Chatmessage,
)

app = FastAPI(title="Moodica API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Moodica backend running", "app": "Moodica"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# --------- Simple utility models ---------
class IdResponse(BaseModel):
    id: str


# --------- Mood Tracking ---------
@app.post("/mood", response_model=IdResponse)
async def create_mood(entry: Moodentry):
    data = entry.model_dump()
    if not data.get("date"):
        data["date"] = datetime.now(timezone.utc)
    _id = create_document("moodentry", data)
    return {"id": _id}


@app.get("/mood", response_model=List[dict])
async def list_moods(limit: int = 30):
    docs = get_documents("moodentry", {}, limit)
    # basic sort by date desc if present
    docs.sort(key=lambda d: d.get("date") or d.get("created_at"), reverse=True)
    # convert ObjectId to str
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return docs


# --------- Worry Release ---------
@app.post("/worry", response_model=IdResponse)
async def create_worry(w: Worry):
    _id = create_document("worry", w)
    return {"id": _id}


@app.get("/worry", response_model=List[dict])
async def list_worries(limit: int = 50):
    docs = get_documents("worry", {}, limit)
    docs.sort(key=lambda d: d.get("created_at"), reverse=True)
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return docs


# --------- Assessments & Plans ---------
@app.post("/assessment", response_model=IdResponse)
async def save_assessment(a: Assessmentresult):
    _id = create_document("assessmentresult", a)
    return {"id": _id}


@app.post("/crisis-plan", response_model=IdResponse)
async def save_crisis_plan(c: Crisisplan):
    _id = create_document("crisisplan", c)
    return {"id": _id}


@app.post("/thought-challenge", response_model=IdResponse)
async def save_thought_challenge(t: Thoughtchallenge):
    _id = create_document("thoughtchallenge", t)
    return {"id": _id}


# --------- Meditation & Calm ---------
@app.post("/meditation", response_model=IdResponse)
async def log_meditation(m: Meditationsession):
    _id = create_document("meditationsession", m)
    return {"id": _id}


# --------- Habits ---------
@app.post("/habit", response_model=IdResponse)
async def create_habit(h: Habit):
    _id = create_document("habit", h)
    return {"id": _id}


@app.post("/habit/log", response_model=IdResponse)
async def log_habit(l: Habitlog):
    _id = create_document("habitlog", l)
    return {"id": _id}


# --------- Recovery ---------
@app.post("/recovery", response_model=IdResponse)
async def create_recovery(r: Recovery):
    _id = create_document("recovery", r)
    return {"id": _id}


@app.post("/recovery/log", response_model=IdResponse)
async def log_recovery(l: Recoverylog):
    _id = create_document("recoverylog", l)
    return {"id": _id}


# --------- Garden & Reflections ---------
@app.post("/garden", response_model=IdResponse)
async def save_garden(g: Garden):
    _id = create_document("garden", g)
    return {"id": _id}


@app.post("/reflection", response_model=IdResponse)
async def save_reflection(r: Reflection):
    _id = create_document("reflection", r)
    return {"id": _id}


# --------- Settings ---------
@app.post("/settings", response_model=IdResponse)
async def save_settings(s: Usersettings):
    _id = create_document("usersettings", s)
    return {"id": _id}


# --------- Chat (placeholder storage only) ---------
@app.post("/chat", response_model=IdResponse)
async def save_chat_message(msg: Chatmessage):
    _id = create_document("chatmessage", msg)
    return {"id": _id}


# --------- Compliance ---------
@app.get("/compliance")
def compliance():
    return {
        "medical": "This app does not diagnose or treat medical conditions.",
        "danger": "Contact emergency services if you are in danger.",
        "advice": "Moodica offers emotional wellness support, not medical advice.",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

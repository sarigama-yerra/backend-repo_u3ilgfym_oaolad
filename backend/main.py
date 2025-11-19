from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from schemas import (
    Usersettings, Moodentry, Worry, Assessmentresult, Crisisplan, Thoughtchallenge,
    Meditationsession, Habit, Habitlog, Recovery, Recoverylog, Garden, Reflection, Chatmessage
)
from database import db, create_document, get_documents

app = FastAPI(title="Moodica API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"ok": True, "service": "moodica"}

@app.get("/test")
def test_db():
    try:
        _ = db()
        if _ is None:
            raise RuntimeError("DB not connected")
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mood endpoints
@app.post("/mood")
def post_mood(entry: Moodentry):
    return create_document("moodentry", entry.dict())

@app.get("/mood")
def get_moods():
    return get_documents("moodentry", limit=100)

# Worry
@app.post("/worry")
def post_worry(w: Worry):
    return create_document("worry", w.dict())

@app.get("/worry")
def get_worries():
    return get_documents("worry", limit=100)

# Assessments
@app.post("/assessment")
def post_assessment(a: Assessmentresult):
    return create_document("assessmentresult", a.dict())

# Crisis plan
@app.post("/crisis-plan")
def post_crisis(cp: Crisisplan):
    return create_document("crisisplan", cp.dict())

# Thought challenge
@app.post("/thought-challenge")
def post_thought(tc: Thoughtchallenge):
    return create_document("thoughtchallenge", tc.dict())

# Meditation
@app.post("/meditation")
def post_meditation(m: Meditationsession):
    return create_document("meditationsession", m.dict())

# Habits
@app.post("/habit")
def post_habit(h: Habit):
    return create_document("habit", h.dict())

@app.post("/habit/log")
def post_habit_log(l: Habitlog):
    return create_document("habitlog", l.dict())

# Recovery
@app.post("/recovery")
def post_recovery(r: Recovery):
    return create_document("recovery", r.dict())

@app.post("/recovery/log")
def post_recovery_log(l: Recoverylog):
    return create_document("recoverylog", l.dict())

# Garden & Reflection
@app.post("/garden")
def post_garden(g: Garden):
    return create_document("garden", g.dict())

@app.post("/reflection")
def post_reflection(r: Reflection):
    return create_document("reflection", r.dict())

# Settings
@app.post("/settings")
def post_settings(s: Usersettings):
    return create_document("usersettings", s.dict())

# Chat companion (stubbed non-AI placeholder storage)
@app.post("/chat")
def post_chat(msg: Chatmessage):
    # Store the user message and return a supportive stub reply
    create_document("chatmessage", msg.dict())
    reply = Chatmessage(role="assistant", content="I'm here with you. Try a slow breath in for 4, hold 4, out for 6. What's one small thing you might try next?" )
    create_document("chatmessage", reply.dict())
    return {"messages": [msg.dict(), reply.dict()]}

@app.get("/compliance")
def compliance():
    return {
        "message": "Moodica is a wellness tool for support and education. It is not a medical device and does not provide diagnosis or treatment. If you are in danger or experiencing a crisis, contact local emergency services immediately.",
    }

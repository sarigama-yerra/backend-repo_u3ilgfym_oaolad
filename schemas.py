"""
Database Schemas for Moodica

Each Pydantic model below maps to a MongoDB collection with the lowercase
class name as the collection name (e.g., MoodEntry -> "moodentry").

These schemas are used for validation before inserting into the database.
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# Core user settings and personalization
class Usersettings(BaseModel):
    theme: Literal["light", "dark"] = Field("light")
    avatar: Optional[str] = Field(None, description="Chosen cloud avatar ID")
    notification_style: Literal["soft", "neutral", "motivational"] = Field("soft")
    ui_tone: Literal["quiet", "happy"] = Field("quiet")
    garden_style: Optional[str] = Field(None, description="Preferred garden appearance preset")

# Mood tracking
class Moodentry(BaseModel):
    mood: int = Field(..., ge=1, le=10, description="Mood level 1-10")
    note: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = Field(default_factory=list)
    date: Optional[datetime] = Field(default=None, description="Date of mood. Defaults to now on server")

# Worry release
class Worry(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    intensity: Optional[int] = Field(None, ge=1, le=10)

# Assessments
class Assessmentresult(BaseModel):
    kind: Literal["anxiety", "stress", "low_mood"]
    score: int = Field(..., ge=0, le=21)
    explanation: Optional[str] = None
    plan: Optional[List[str]] = None

# Crisis plan
class Crisisplan(BaseModel):
    title: str = Field(..., max_length=100)
    steps: List[str] = Field(...)
    contacts: Optional[List[str]] = None

# CBT Thought challenge
class Thoughtchallenge(BaseModel):
    situation: str
    thought: str
    evidence_for: Optional[str] = None
    evidence_against: Optional[str] = None
    reframe: Optional[str] = None

# Meditation & Calm
class Meditationsession(BaseModel):
    kind: Literal["breathing", "mindfulness", "sleep", "music"]
    duration_min: int = Field(..., ge=1, le=120)
    notes: Optional[str] = None

# Habits
class Habit(BaseModel):
    title: str
    frequency: Literal["daily", "weekly"] = "daily"
    type: Literal["build", "reduce"] = "build"

class Habitlog(BaseModel):
    habit_id: str
    status: Literal["done", "skipped"] = "done"

# Recovery
class Recovery(BaseModel):
    target: str = Field(..., description="Habit user wants to stop")
    start_date: Optional[datetime] = None
    reason: Optional[str] = None

class Recoverylog(BaseModel):
    recovery_id: str
    day: int = Field(..., ge=0)
    trigger: Optional[str] = None
    status: Literal["kept", "lapsed"] = "kept"

# Growth Garden
class Garden(BaseModel):
    gratitude: Optional[List[str]] = Field(default_factory=list)
    proud_moments: Optional[List[str]] = Field(default_factory=list)
    safe_place: Optional[str] = None

class Reflection(BaseModel):
    text: str
    reveal_at: Optional[datetime] = None

# Companion chat messages (stored optionally)
class Chatmessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    conversation_id: Optional[str] = None

"""
Note: The Flames database viewer can read these schemas via the /schema endpoint.
"""

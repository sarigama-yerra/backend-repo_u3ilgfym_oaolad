from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Each model -> collection with the class name lowercased
class Usersettings(BaseModel):
    user_id: Optional[str] = None
    theme: Optional[str] = Field(default="dark", description="light|dark")
    avatar: Optional[str] = None
    notification_style: Optional[str] = None

class Moodentry(BaseModel):
    user_id: Optional[str] = None
    mood: int = Field(ge=1, le=10)
    note: Optional[str] = None
    date: Optional[str] = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))

class Worry(BaseModel):
    user_id: Optional[str] = None
    text: str
    resolved: bool = False

class Assessmentresult(BaseModel):
    user_id: Optional[str] = None
    kind: str
    score: int
    level: Optional[str] = None
    notes: Optional[str] = None

class Crisisplan(BaseModel):
    user_id: Optional[str] = None
    contacts: List[str] = []
    steps: List[str] = []

class Thoughtchallenge(BaseModel):
    user_id: Optional[str] = None
    situation: str
    thought: str
    evidence_for: Optional[str] = None
    evidence_against: Optional[str] = None
    reframe: Optional[str] = None

class Meditationsession(BaseModel):
    user_id: Optional[str] = None
    kind: str
    duration_sec: int

class Habit(BaseModel):
    user_id: Optional[str] = None
    title: str
    frequency: str = "daily"

class Habitlog(BaseModel):
    user_id: Optional[str] = None
    habit_id: str
    date: str

class Recovery(BaseModel):
    user_id: Optional[str] = None
    behavior: str
    pledge: Optional[str] = None

class Recoverylog(BaseModel):
    user_id: Optional[str] = None
    recovery_id: str
    date: str
    note: Optional[str] = None

class Garden(BaseModel):
    user_id: Optional[str] = None
    gratitude: Optional[str] = None
    proud_moment: Optional[str] = None

class Reflection(BaseModel):
    user_id: Optional[str] = None
    prompt: str
    text: str

class Chatmessage(BaseModel):
    user_id: Optional[str] = None
    role: str
    content: str

from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_id: str = Field(index=True, unique=True)
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True) # Will map to clerk_id for simplicity
    title: str
    description: Optional[str] = None
    is_completed: bool = Field(default=False)
    priority: int = Field(default=1) # 1: Low, 2: Medium, 3: High
    estimated_time_minutes: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EnergyLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    score: int = Field(ge=0, le=100) # 0-100 energy score
    mood: Optional[str] = None
    sleep_hours: Optional[float] = None
    logged_at: datetime = Field(default_factory=datetime.utcnow)

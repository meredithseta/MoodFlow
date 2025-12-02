from pydantic import BaseModel
from datetime import date
from typing import Optional

class MoodLog(BaseModel):
    mood_id: Optional[int] = None
    user_id: int
    mood: str
    log_date: date
    sleep_hours: float
    water_intake: float

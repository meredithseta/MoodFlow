from pydantic import BaseModel
from datetime import date

class SleepCreate(BaseModel):
    user_id: int
    date: date
    hours_slept: float
    quality_score: int
    dream_intensity: int

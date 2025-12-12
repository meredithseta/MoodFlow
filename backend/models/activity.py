from pydantic import BaseModel

class ActivityCreate(BaseModel):
    user_id: int
    activity_id: int
    duration_minutes: int
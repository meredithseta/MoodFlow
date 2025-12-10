from pydantic import BaseModel

class MoodCreate(BaseModel):
    user_id: int
    mood_type_id: int
    mood_color_hex: str
    stress_level: int
    notes: str | None = None

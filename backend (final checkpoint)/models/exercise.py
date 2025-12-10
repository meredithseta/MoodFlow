from pydantic import BaseModel

class ExerciseCreate(BaseModel):
    user_id: int
    exercise_id: int
    notes: str | None = None

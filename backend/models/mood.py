from pydantic import BaseModel
from fastapi import APIRouter
import datetime
from database.connection import get_connection

router = APIRouter(prefix="/mood", tags=["Mood"])

@router.get("/types")
def get_mood_types():
    conn = get_connection()
    cur = conn.cursor(dictionary = True)

    cur.execute("SELECT * FROM Mood_types ORDER BY mood_intensity")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

class MoodCreate(BaseModel):
    user_id: int
    mood_type_id: int
    log_date: datetime.date
    mood_color_hex: str
    stress_level: int
    notes: str | None = None

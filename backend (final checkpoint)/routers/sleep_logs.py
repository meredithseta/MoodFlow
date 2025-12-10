from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from database.connection import get_connection, log_audit_action

router = APIRouter(prefix="/sleep", tags=["Sleep Logs"])

class SleepCreate(BaseModel):
    user_id: int
    date: date
    hours_slept: float
    quality_score: int
    dream_intensity: int


# CREATE
@router.post("/")
def create_sleep(sleep: SleepCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Sleep_quality (user_id, date, hours_slept, quality_score, dream_intensity)
        VALUES (%s,%s,%s,%s,%s)
    """, (sleep.user_id, sleep.date, sleep.hours_slept, sleep.quality_score, sleep.dream_intensity))

    new_id = cur.lastrowid
    conn.commit()

    # AUDIT LOG
    log_audit_action(sleep.user_id, "INSERT", "Sleep_quality", new_id)

    cur.close()
    conn.close()
    return {"message": "Sleep log added", "sleep_quality_id": new_id}


# GET ALL FOR USER
@router.get("/{user_id}")
def get_sleep(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM Sleep_quality WHERE user_id = %s ORDER BY date DESC", (user_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

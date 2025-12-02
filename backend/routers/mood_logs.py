from fastapi import APIRouter, HTTPException
from database.connection import get_connection
from models.mood_logs import MoodLog

router = APIRouter(prefix="/mood_logs", tags=["Mood Logs"])


# READ all logs
@router.get("/")
def get_all_logs():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM mood_logs")
    result = cur.fetchall()
    conn.close()
    return result


# FILTER by mood
@router.get("/filter")
def filter_logs(mood: str):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM mood_logs WHERE mood = %s", (mood,))
    result = cur.fetchall()
    conn.close()
    return result


# CREATE
@router.post("/")
def create_log(log: MoodLog):
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO mood_logs (user_id, mood, log_date, sleep_hours, water_intake)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        log.user_id,
        log.mood,
        log.log_date,
        log.sleep_hours,
        log.water_intake
    )

    cur.execute(sql, values)
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {"message": "Mood log created.", "mood_id": new_id}


# UPDATE
@router.put("/{mood_id}")
def update_log(mood_id: int, log: MoodLog):
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        UPDATE mood_logs
        SET user_id = %s,
            mood = %s,
            log_date = %s,
            sleep_hours = %s,
            water_intake = %s
        WHERE mood_id = %s
    """

    values = (
        log.user_id,
        log.mood,
        log.log_date,
        log.sleep_hours,
        log.water_intake,
        mood_id
    )

    cur.execute(sql, values)
    conn.commit()
    conn.close()

    return {"message": "Mood log updated."}


# DELETE
@router.delete("/{mood_id}")
def delete_log(mood_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM mood_logs WHERE mood_id = %s", (mood_id,))
    conn.commit()
    conn.close()
    return {"message": "Mood log deleted."}

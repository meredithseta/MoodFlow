from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import datetime
from database.connection import get_connection, log_audit_action
from models.mood import MoodCreate

router = APIRouter(prefix="/mood_logs", tags=["Mood Logs"])

# Get mood types
@router.get("/types")
def get_mood_types():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM Mood_types ORDER BY mood_intensity")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

#Create mood log
@router.post("/")
def create_mood_log(mood: MoodCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Mood_log (user_id, mood_type_id, log_date, mood_color_hex, stress_level, notes)
        VALUES (%s, %s, NOW(), %s, %s, %s)
    """, (mood.user_id, mood.mood_type_id, mood.mood_color_hex, mood.stress_level, mood.notes))

    conn.commit()
    new_id = cur.lastrowid

    log_audit_action(mood.user_id, "INSERT", "Mood_log", new_id)

    cur.close()
    conn.close()
    return {"message": "Mood log created", "mood_log_id": new_id}

# Read logs for a user
@router.get("/{user_id}")
def get_mood_logs(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT m.*, t.mood_name, t.mood_intensity
        FROM Mood_log m
        JOIN Mood_types t ON m.mood_type_id = t.mood_type_id
        WHERE m.user_id = %s
        ORDER BY m.log_date DESC
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

# Update mood log
@router.put("/{mood_log_id}")
def update_mood_log(mood_log_id: int, mood: MoodCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM Mood_log WHERE mood_log_id = %s", (mood_log_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Mood log not found")

    cur.execute("""
        UPDATE Mood_log
        SET mood_type_id = %s,
            mood_color_hex = %s,
            stress_level = %s,
            notes = %s
        WHERE mood_log_id = %s
    """, (mood.mood_type_id, mood.mood_color_hex, mood.stress_level, mood.notes, mood_log_id))

    conn.commit()

    log_audit_action(row[0], "UPDATE", "Mood_log", mood_log_id)

    cur.close()
    conn.close()
    return {"message": "Mood log updated"}

# Delete mood log
@router.delete("/{mood_log_id}")
def delete_mood_log(mood_log_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT user_id FROM Mood_log WHERE mood_log_id = %s", (mood_log_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Mood log not found")

    user_id = row["user_id"]

    cur.execute("DELETE FROM Mood_log WHERE mood_log_id = %s", (mood_log_id,))
    conn.commit()

    log_audit_action(user_id, "DELETE", "Mood_log", mood_log_id)

    cur.close()
    conn.close()
    return {"message": "Mood log deleted"}
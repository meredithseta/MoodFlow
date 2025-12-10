from fastapi import APIRouter, HTTPException
from database.connection import get_connection, log_audit_action
from models.mood import MoodCreate

router = APIRouter(prefix="/mood", tags=["Mood Logs"])

# CREATE
@router.post("/")
def create_mood(mood: MoodCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Mood_log (user_id, mood_type_id, mood_color_hex, stress_level, notes)
        VALUES (%s, %s, %s, %s, %s)
    """, (mood.user_id, mood.mood_type_id, mood.mood_color_hex, mood.stress_level, mood.notes))

    conn.commit()
    new_id = cur.lastrowid

    # AUDIT LOG
    log_audit_action(mood.user_id, "INSERT", "Mood_log", new_id)

    cur.close()
    conn.close()

    return {"message": "Mood log created", "mood_log_id": new_id}


# READ ALL FOR A USER
@router.get("/{user_id}")
def get_moods(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT m.*, t.mood_name, t.mood_intensity
        FROM Mood_log m
        JOIN Mood_types t ON m.mood_type_id = t.mood_type_id
        WHERE m.user_id = %s
        ORDER BY m.log_date DESC
    """, (user_id,))

    result = cur.fetchall()

    cur.close()
    conn.close()
    return result


# UPDATE
@router.put("/{mood_log_id}")
def update_mood(mood_log_id: int, mood: MoodCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Mood_log WHERE mood_log_id = %s", (mood_log_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Mood log not found")

    cur.execute("""
        UPDATE Mood_log
        SET mood_type_id=%s,
            mood_color_hex=%s,
            stress_level=%s,
            notes=%s
        WHERE mood_log_id=%s
    """, (mood.mood_type_id, mood.mood_color_hex, mood.stress_level, mood.notes, mood_log_id))

    conn.commit()

    # AUDIT LOG
    log_audit_action(mood.user_id, "UPDATE", "Mood_log", mood_log_id)

    cur.close()
    conn.close()

    return {"message": "Mood log updated"}


# DELETE
@router.delete("/{mood_log_id}")
def delete_mood(mood_log_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM Mood_log WHERE mood_log_id=%s", (mood_log_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Mood log not found")

    user_id = row[0]

    cur.execute("DELETE FROM Mood_log WHERE mood_log_id = %s", (mood_log_id,))
    conn.commit()

    # AUDIT LOG
    log_audit_action(user_id, "DELETE", "Mood_log", mood_log_id)

    cur.close()
    conn.close()

    return {"message": "Mood log deleted"}

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import get_connection

router = APIRouter(prefix="/exercise", tags=["Exercise Logs"])

class ExerciseCreate(BaseModel):
    user_id: int
    exercise_id: int
    notes: str | None = None

class ExerciseUpdate(BaseModel):
    notes: str | None = None
    completed: bool | None = None


# CREATE
@router.post("/")
def log_exercise(ex: ExerciseCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO User_exercise_log (user_id, exercise_id, notes)
        VALUES (%s, %s, %s)
    """, (ex.user_id, ex.exercise_id, ex.notes))

    conn.commit()
    new_id = cur.lastrowid

    cur.close()
    conn.close()
    return {"message": "Exercise logged", "user_exercise_id": new_id}


# READ (all exercise logs for a user)
@router.get("/{user_id}")
def get_exercise_logs(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT uel.*, e.exercise_name, e.category
        FROM User_exercise_log uel
        JOIN Mindfulness_exercises e ON uel.exercise_id = e.exercise_id
        WHERE uel.user_id = %s
        ORDER BY uel.date DESC
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


# UPDATE (notes or completed)
@router.put("/{log_id}")
def update_exercise(log_id: int, update: ExerciseUpdate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM User_exercise_log WHERE user_exercise_id = %s", (log_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Exercise log not found")

    cur.execute("""
        UPDATE User_exercise_log
        SET notes = %s,
            completed = %s
        WHERE user_exercise_id = %s
    """, (update.notes, update.completed, log_id))

    conn.commit()

    cur.close()
    conn.close()
    return {"message": "Exercise log updated"}


# DELETE
@router.delete("/{log_id}")
def delete_exercise(log_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM User_exercise_log WHERE user_exercise_id = %s", (log_id,))
    conn.commit()

    cur.close()
    conn.close()
    return {"message": "Exercise log deleted"}

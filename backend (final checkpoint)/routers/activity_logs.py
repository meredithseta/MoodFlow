from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import get_connection

router = APIRouter(prefix = "/activity", tags = ["Activity Logs"])

class ActivityCreate(BaseModel):
    user_id: int
    activity_id: int
    duration_minutes: int

class ActivityUpdate(BaseModel):
    duration_minutes: int

# Create
@router.post("/")
def create_activity(activity: ActivityCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Activity_log (user_id, activity_id, duration_minutes)
        VALUES (%s,%s,%s)
    """, (activity.user_id, activity.activity_id, activity.duration_minutes))

    conn.commit()
    new_id = cur.lastrowid

    cur.close()
    conn.close()
    return {"message": "Activity logged", "activity_log_id": new_id}


# Read all activity logs for a user
@router.get("/{user_id}")
def get_activity(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary = True)

    cur.execute("""
        SELECT a.*, t.activity_name, t.category
        FROM Activity_log a
        JOIN Activity_types t ON a.activity_id = t.activity_id
        WHERE user_id = %s
        ORDER BY log_date DESC
    """, (user_id,))
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# Update
@router.put("/{activity_log_id}")
def update_activity(activity_log_id: int, data: ActivityUpdate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Activity_log WHERE activity_log_id = %s", (activity_log_id,))
    if not cur.fetchone():
        raise HTTPException(status_code = 404, detail = "Activity log not found")

    cur.execute("""
        UPDATE Activity_log
        SET duration_minutes = %s
        WHERE activity_log_id = %s
    """, (data.duration_minutes, activity_log_id))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Activity log updated"}


# Delete
@router.delete("/{activity_log_id}")
def delete_activity(activity_log_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM Activity_log WHERE activity_log_id = %s", (activity_log_id,))
    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Activity log deleted"}

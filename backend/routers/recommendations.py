from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import get_connection

router = APIRouter(prefix = "/recommendations", tags = ["Recommendations"])

class FeedbackCreate(BaseModel):
    user_recommendation_id: int
    was_helpful: bool

class RecommendationAssign(BaseModel):
    user_id: int
    recommendation_id: int

# Get recommendations by mood
@router.get("/{mood_type_id}")
def get_recommendations(mood_type_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary = True)

    cur.execute("""
        SELECT recommendation_id, category, description
        FROM Recommendation
        WHERE mood_trigger_id = %s
    """, (mood_type_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

# Assign a recommendation to a user
@router.post("/assign")
def assign_recommendation(data: RecommendationAssign):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO User_recommendation (user_id, recommendation_id)
        VALUES (%s, %s)
    """, (data.user_id, data.recommendation_id))

    conn.commit()
    new_id = cur.lastrowid

    cur.close()
    conn.close()

    return {"message": "Recommendation assigned to user", "user_recommendation_id": new_id}

# Store feedback
@router.post("/feedback")
def feedback(fb: FeedbackCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM User_recommendation
        WHERE user_recommendation_id = %s
    """, (fb.user_recommendation_id,))
    
    if not cur.fetchone():
        raise HTTPException(status_code = 404, detail = "User recommendation ID not found")

    cur.execute("""
        INSERT INTO Recommendation_feedback (user_recommendation_id, was_helpful)
        VALUES (%s, %s)
    """, (fb.user_recommendation_id, fb.was_helpful))

    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Feedback saved"}
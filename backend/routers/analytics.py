from fastapi import APIRouter
import mysql.connector
import pandas as pd

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="moodflow"
    )

@router.get("/sleep-vs-happiness")
def sleep_vs_happiness():
    conn = get_conn()
    query = """
        SELECT sleep_hours AS sleep, happiness_score AS happiness
        FROM Lifestyle_data
        WHERE sleep_hours IS NOT NULL AND happiness_score IS NOT NULL
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient="records")

@router.get("/stress-lifestyle")
def stress_lifestyle():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                exercise_level AS exercise,
                ROUND(AVG(stress_level),2) AS avg_stress,
                ROUND(AVG(happiness_score),2) AS avg_happiness,
                COUNT(*) AS sample_size
            FROM Lifestyle_data
            GROUP BY exercise_level
            ORDER BY avg_stress DESC;
        """)

        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return {"lifestyle_stress_summary": data}

    except Exception as e:
        return {"error": str(e)}


@router.get("/mood-change-by-activity")
def mood_change_by_activity():
    conn = get_conn()
    query = """
        SELECT activity, mood_before, mood_after,
               (mood_after - mood_before) AS mood_change
        FROM fitlife_data
        WHERE mood_before IS NOT NULL AND mood_after IS NOT NULL
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient="records")

@router.get("/health-summary")
def health_summary():
    conn = get_conn()
    query = """
        SELECT gender, AVG(hours_slept) AS sleep_avg,
               AVG(water_intake_l) AS water_avg,
               AVG(steps_taken) AS steps_avg,
               AVG(stress_level) AS stress_avg
        FROM health_data GROUP BY gender
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient="records")

@router.get("/recommend/{mood}")
def recommend(mood: str):
    mood = mood.lower()

    if mood in ["stressed", "anxious"]:
        return {"recommendations": ["Deep breathing", "Walk outside", "Reduce screen time"]}

    if mood in ["sad", "down"]:
        return {"recommendations": ["Listen to music", "Talk to a friend", "Light exercise"]}

    if mood in ["happy", "energetic"]:
        return {"recommendations": ["Workout challenge", "Creative hobby", "Goal setting"]}

    return {"recommendations": ["Drink water", "Take a stretch break", "Relax for 5 minutes"]}

from fastapi import APIRouter
import mysql.connector
import pandas as pd

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="moodflow"
    )

@router.get("/{mood}/{sleep}/{water}")
def recommend_user(mood: str, sleep: float, water: float):
    """
    Returns AI-like smart recommendation based on real datasets + user log input.
    """

    conn = get_conn()

    # Pull average patterns from datasets ---
    life = pd.read_sql("SELECT * FROM lifestyle_data", conn)
    fit = pd.read_sql("SELECT * FROM fitlife_data", conn)
    health = pd.read_sql("SELECT * FROM health_data", conn)
    conn.close()

    recs = []  # final suggestion list

    # Mood-based suggestions using fitlife dataset 
    mood_effect = fit.groupby("activity")["Mood After (1-10)"].mean().sort_values(ascending=False)

    top_good_activities = mood_effect.head(3).index.tolist()

    if mood.lower() in ["sad", "down", "low", "tired"]:
        recs.append(f"People with similar moods felt better after: {top_good_activities[0]}")
    
    if mood.lower() in ["stressed", "anxious", "overwhelmed"]:
        recs.append("Stress detected → Try deep breathing or a short walk outdoors")

    #  Sleep-based 
    if sleep < 6:
        recs.append("Low sleep → consider winding down 1hr earlier or reducing screen time before bed")
    else:
        recs.append("Good sleep habits detected — keep it up!")

    # Water intake 
    if water < 50:
        recs.append("Hydration low → aim for +1 bottle of water today")
    else:
        recs.append("Hydration level healthy")

    #  Data-driven trend from lifestyle dataset
    avg = life.groupby("exercise_level")["happiness_score"].mean().idxmax()
    recs.append(f"Users with highest happiness reported: **{avg.lower()} exercise levels**")

    return {"recommendations": recs}

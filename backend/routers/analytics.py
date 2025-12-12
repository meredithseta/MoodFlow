from fastapi import APIRouter, HTTPException
from database.connection import get_connection

router = APIRouter(prefix = "/analytics", tags = ["Analytics"])

# Mood vs Sleep
@router.get("/mood-vs-sleep/{user_id}")
def mood_vs_sleep(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary = True)

    cur.execute("""
        SELECT 
            s.date,
            s.hours_slept,
            m.stress_level,
            t.mood_name,
            m.notes
        FROM Sleep_quality s
        JOIN Mood_log m ON DATE(m.log_date) = s.date AND m.user_id = s.user_id
        JOIN Mood_types t ON m.mood_type_id = t.mood_type_id
        WHERE s.user_id = %s
        ORDER BY s.date DESC;
    """, (user_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()

    return data


# Weekly Trends
@router.get("/weekly-trends/{user_id}")
def weekly_trends(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary = True)

    cur.execute("""
        SELECT 
            YEARWEEK(log_date, 1) AS week,
            COUNT(*) AS total_entries,
            AVG(stress_level) AS avg_stress,
            AVG(mt.mood_intensity) AS avg_intensity
        FROM Mood_log ml
        JOIN Mood_types mt ON ml.mood_type_id = mt.mood_type_id
        WHERE ml.user_id = %s
        GROUP BY YEARWEEK(log_date, 1)
        ORDER BY week DESC
        LIMIT 10;
    """, (user_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


# Lifestyle correlation
@router.get("/lifestyle-correlation")
def lifestyle_correlation():
    conn = get_connection()
    cur = conn.cursor(dictionary = True)

    cur.execute("""
        SELECT 
            age_group,
            AVG(sleep_hours_avg) AS sleep_avg,
            AVG(stress_level) AS stress_avg,
            AVG(happiness_index) AS happiness_avg,
            AVG(exercise_frequency) AS exercise_freq
        FROM Lifestyle_data
        GROUP BY age_group
        ORDER BY age_group;
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


# Activity impact on mood
@router.get("/activity-impact/{user_id}")
def activity_impact(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary = True)

    cur.execute("""
        SELECT 
            at.activity_name,
            AVG(ml.stress_level) AS avg_stress_after,
            COUNT(*) AS occurrences
        FROM Activity_log al
        JOIN Activity_types at ON al.activity_id = at.activity_id
        JOIN Mood_log ml 
            ON ml.user_id = al.user_id
           AND ml.log_date >= al.log_date
           AND ml.log_date <= DATE_ADD(al.log_date, INTERVAL 3 HOUR)
        WHERE al.user_id = %s
        GROUP BY at.activity_name
        ORDER BY avg_stress_after ASC;
    """, (user_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


# Exercise impact on mood
@router.get("/exercise-impact/{user_id}")
def exercise_impact(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary = True)

    cur.execute("""
        SELECT 
            e.exercise_name,
            AVG(ml.stress_level) AS avg_stress_after,
            COUNT(*) AS uses
        FROM User_exercise_log uel
        JOIN Mindfulness_exercises e ON uel.exercise_id = e.exercise_id
        JOIN Mood_log ml ON ml.user_id = uel.user_id
            AND ml.log_date >= uel.date
            AND ml.log_date <= DATE_ADD(uel.date, INTERVAL 2 HOUR)
        WHERE uel.user_id = %s
        GROUP BY e.exercise_name
        ORDER BY avg_stress_after ASC;
    """, (user_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


# Daily summary
@router.get("/daily-summary/{user_id}")
def daily_summary(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary = True)

    cur.execute("""
        SELECT 
            date,
            avg_mood,
            total_sleep,
            total_steps,
            avg_stress
        FROM User_daily_summary
        WHERE user_id = %s
        ORDER BY date DESC
        LIMIT 30;
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

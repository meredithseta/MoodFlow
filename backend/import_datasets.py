import pandas as pd
import numpy as np
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="moodflow"
)
cursor = conn.cursor()

def map_exercise_level(value):
    if value is None:
        return 0
    v = str(value).lower()
    if v == "low":
        return 1
    elif v == "medium":
        return 3
    elif v == "high":
        return 5
    else:
        return 0


def age_to_group(age):
    if age is None:
        return None
    try:
        age = int(age)
    except:
        return None
    if age < 25:
        return "18-24"
    elif age < 35:
        return "25-34"
    elif age < 50:
        return "35-49"
    else:
        return "50+"

def map_stress(value):
    if isinstance(value, str):
        value = value.lower().strip()
        return {"low": 3, "medium": 6, "high": 9}.get(value, None)
    return value

print("\nImporting Lifestyle_data into schema")

df_life = pd.read_csv("datasets/lifestyle.csv").replace({np.nan: None})

for _, r in df_life.iterrows():
    cursor.execute("""
        INSERT INTO Lifestyle_data
            (age_group, gender, sleep_hours_avg, exercise_frequency,
             diet_quality_score, happiness_index, stress_level)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        age_to_group(r.get("Age")),
        r.get("Gender"),
        r.get("Sleep Hours"),
        map_exercise_level(r.get("Exercise Level")),
        None,
        r.get("Happiness Score"),
        map_stress(r.get("Stress Level"))
    ))

# Import fitlife into fitness_tracking
print("\nImporting FitLife dataset into Fitness_Tracking")

df_fit = pd.read_csv("datasets/fitlife.csv").replace({np.nan: None})

base_date = pd.to_datetime("2025-01-01")

for _, r in df_fit.iterrows():
    raw_date = r.get("Date")

    try:
        days_offset = int(raw_date)
        fitlife_date = (base_date + pd.to_timedelta(days_offset, unit="D")).date()
    except:
        fitlife_date = None

    cursor.execute("""
        INSERT INTO Fitness_Tracking
            (date, steps, calories, sleep_hours, water_intake,
            heart_rate, mood, stress_level)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        fitlife_date,
        0,
        0,
        0,
        0,
        0,  
        r.get("Primary Emotion"),
        r.get("Stress Level (1-10)")
    ))

# Import health dataset into fitness_tracking
print("\nImporting health.xlsx dataset into Fitness_Tracking")

df_health = pd.read_excel("datasets/health.xlsx").replace({np.nan: None})

for _, r in df_health.iterrows():

    mood = r.get("mood")
    if mood is None:
        mood = "Unknown"

    cursor.execute("""
        INSERT INTO Fitness_Tracking
            (date, steps, calories, sleep_hours, water_intake,
             heart_rate, mood, stress_level)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        r.get("date") or r.get("Date"),
        r.get("steps_taken"),
        r.get("calories_burn"),
        r.get("hours_slept"),
        r.get("water_intake_l"),
        r.get("heart_rate_bpm"),
        mood,
        r.get("stress_level")
    ))


conn.commit()
cursor.close()
conn.close()

print("\nAll dataset imports completed successfully\n")

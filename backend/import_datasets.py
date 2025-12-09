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


def map_stress(value):
    if isinstance(value, str):
        value = value.strip().lower()
        return {"low": 3, "medium": 6, "high": 9}.get(value, None)
    return value   # if already numeric


print("\n=== Importing lifestyle.csv ===")
df1 = pd.read_csv("datasets/lifestyle.csv").replace({np.nan: None})
for _, r in df1.iterrows():
    cursor.execute("""
        INSERT INTO Lifestyle_data
        (country, age, gender, exercise_level, diet_type, sleep_hours, stress_level,
         mental_health_condition, work_hours_per_week, screen_time_per_day,
         social_interaction_score, happiness_score)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        r['Country'], r['Age'], r['Gender'], r['Exercise Level'], r['Diet Type'],
        r['Sleep Hours'], map_stress(r['Stress Level']), r['Mental Health Condition'],
        r['Work Hours per Week'], r['Screen Time per Day (Hours)'],
        r['Social Interaction Score'], r['Happiness Score']
    ))

print("\n=== Importing fitlife.csv ===")
df2 = pd.read_csv("datasets/fitlife.csv").replace({np.nan: None})

for _, r in df2.iterrows():
    cursor.execute("""
        INSERT INTO fitlife_data
        (date, age, gender, time_of_day, activity_category, sub_category, activity,
         duration_minutes, intensity, primary_emotion, secondary_emotion,
         mood_before, mood_after, energy_level, stress_level)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        r['ID'],                   # DATE actually here
        r['Date'],                 # AGE here
        r['Age'],                  # GENDER here
        r['Gender'],               # TIME OF DAY here
        r['Activity Category'],
        r['Sub-Category'],
        r['Activity'],
        r['Duration (minutes)'],
        r['Intensity'],
        r['Primary Emotion'],
        r['Secondary Emotion'],
        r['Mood Before (1-10)'],
        r['Mood After (1-10)'],
        r['Energy Level (1-10)'],
        r['Stress Level (1-10)']
    ))



print("\n=== Importing health.xlsx ===")
df3 = pd.read_excel("datasets/health.xlsx").replace({np.nan: None})
for _, r in df3.iterrows():
    cursor.execute("""
        INSERT INTO health_data
        (user_id, full_name, date, age, gender, height_cm, weight_kg, steps_taken,
         calories_burn, hours_slept, water_intake_l, active_minutes,
         heart_rate_bpm, workout_type, stress_level, mood)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(r.values))

conn.commit()
cursor.close()
conn.close()
print("\nAll datasets imported successfully\n")

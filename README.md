# MoodFlow
CS 3620 Team Project - Mood Tracker App
Meredith Seta & Seth Nelson

Public Datasets Used:
1. Mental Health and Lifestyle Habits Dataset (2019-2024)
    - Source: Kaggle
    - Link: https://www.kaggle.com/datasets/atharvasoundankar/mental-health-and-lifestyle-habits-2019-2024?utm_source=chatgpt.com

2. FitLife Emotions, Mood & Activity Dataset
    - Source: Kaggle
    - Link: https://www.kaggle.com/datasets/jijagallery/fitlife-emotions-mood-and-activity-dataset?utm_source=chatgpt.com

3. Comprehensive Fitness & Health Tracking Dataset
    - Source: Kaggle
    - Link: https://www.kaggle.com/datasets/siddheshtoraskar/comprehensive-fitness-and-health-tracking-dataset?utm_source=chatgpt.com

Setup/Run Instructions (Run these in order):
1. cd backend/database
2. mysql -u root -p
    - user: root
    - password: root
3. SOURCE moodflow_schema.sql;
4. USE moodflow;
5. EXIT;
6. cd ..
7. pip install fastapi uvicorn mysql-connector-python pandas openpyxl
8. python3 import_datasets.py
9. uvicorn main:app --reload
    - API root: http://127.0.0.1:8000
    - Swagger UI: http://127.0.0.1:8000/docs
10. cd ../frontend
11. npm install
12. npm start
    - Frontend UI: http://localhost:3000
    - If it loads or spins forever, try running it in an incognito window.
      Google extensions were giving me issues running it, but it worked in incognito.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.users import router as users_router
from routers.mood_logs import router as mood_router
from routers.sleep_logs import router as sleep_router
from routers.activity_logs import router as activity_router
from routers.exercises import router as exercise_router
from routers.recommendations import router as recommendations_router
from routers.analytics import router as analytics_router

app = FastAPI(title="MoodFlow Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users_router)
app.include_router(mood_router)
app.include_router(sleep_router)
app.include_router(activity_router)
app.include_router(exercise_router)
app.include_router(recommendations_router)
app.include_router(analytics_router)

@app.get("/")
def root():
    return {"message": "MoodFlow backend is running!"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.mood_logs import router as mood_logs_router

app = FastAPI(title="MoodFlow Backend - Checkpoint 2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(mood_logs_router)

@app.get("/")
def root():
    return {"message": "MoodFlow backend is running!"}

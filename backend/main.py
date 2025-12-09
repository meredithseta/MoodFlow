from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routers.mood_logs import router as mood_logs_router
from routers.recommend import router as recommend_router   # <-- import recommendation router

app = FastAPI(title="MoodFlow Backend - Checkpoint 2")

# CORS allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# REGISTER ROUTES AFTER APP IS CREATED
app.include_router(mood_logs_router)
app.include_router(recommend_router)  # <-- must come AFTER app = FastAPI()

@app.get("/")
def root():
    return {"message": "MoodFlow backend running successfully"}

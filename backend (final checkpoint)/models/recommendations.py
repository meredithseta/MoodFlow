from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    user_recommendation_id: int
    was_helpful: bool

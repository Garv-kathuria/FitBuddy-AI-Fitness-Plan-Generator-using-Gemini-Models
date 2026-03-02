from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, description="User's full name")
    age: int = Field(..., gt=0, lt=120, description="Age must be between 1 and 120")
    weight: float = Field(..., gt=0, description="Weight in kg must be greater than 0")
    goal: str = Field(..., description="Fitness goal, e.g., weight loss")
    intensity: str = Field(..., description="Workout intensity, e.g., high")

class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True

class FeedbackSubmit(BaseModel):
    feedback: str = Field(..., min_length=5, description="User's feedback to adjust the plan")

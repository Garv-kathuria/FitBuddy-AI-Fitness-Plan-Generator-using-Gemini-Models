from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# The local SQLite database file - pointing to the root directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./fitbuddy.db"

# create_engine connects to the database. 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal will be used in our routes to talk to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the class our database models will inherit from
Base = declarative_base()

# Dependency helper to get the DB session in our FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Models ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)        # e.g., "weight loss", "muscle gain"
    intensity = Column(String)   # e.g., "low", "medium", "high"

    # Links a user to their workout plans (One-to-Many relationship)
    plans = relationship("WorkoutPlan", back_populates="owner")

class WorkoutPlan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    original_plan_content = Column(Text) # Stores the initial 7-day plan
    plan_content = Column(Text)  # Stores the latest 7-day plan (may be updated)
    nutrition_tip = Column(Text) # Stores the targeted nutrition/recovery tip

    # Links the plan back to the user
    owner = relationship("User", back_populates="plans")

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import markdown

from app.database import get_db, User, WorkoutPlan
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Renders the initial user input form."""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request, db: Session = Depends(get_db)):
    """Admin View: Fetches all users and their plans."""
    users = db.query(User).all()
    return templates.TemplateResponse("all_users.html", {
        "request": request,
        "users": users
    })

@router.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    """Scenario 1 & 3: Creates a user, generates a new plan & tip, and saves to DB."""
    
    # 1. Save User to DB
    new_user = User(name=name, age=age, weight=weight, goal=goal, intensity=intensity)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 2. Call Gemini AI via our helper functions
    raw_plan = generate_workout_gemini(name, age, weight, goal, intensity)
    raw_tip = generate_nutrition_tip_with_flash(goal)

    # 3. Save Plan to DB
    new_plan = WorkoutPlan(
        user_id=new_user.id, 
        original_plan_content=raw_plan, 
        plan_content=raw_plan, 
        nutrition_tip=raw_tip
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    # 4. Convert AI Markdown output to clean HTML for the frontend
    html_plan = markdown.markdown(raw_plan)
    html_tip = markdown.markdown(raw_tip)

    # 5. Render Result Page
    return templates.TemplateResponse("result.html", {
        "request": request, 
        "plan_html": html_plan, 
        "tip_html": html_tip,
        "plan_id": new_plan.id,
        "user_name": name
    })

@router.post("/feedback/{plan_id}", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    plan_id: int,
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    """Scenario 2: Accepts feedback, modifies the existing plan via AI, and updates the DB."""
    
    # 1. Fetch the existing plan from the DB
    db_plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
    if not db_plan:
        return HTMLResponse("Plan not found", status_code=404)
    
    # 2. Call Gemini AI to update the plan
    updated_raw_plan = update_workout_plan(db_plan.plan_content, feedback)
    
    # 3. Update the Database record
    db_plan.plan_content = updated_raw_plan
    db.commit()
    db.refresh(db_plan)

    # 4. Convert to HTML for display
    html_plan = markdown.markdown(updated_raw_plan)
    html_tip = markdown.markdown(db_plan.nutrition_tip) # Keep the existing tip

    return templates.TemplateResponse("result.html", {
        "request": request,
        "plan_html": html_plan,
        "tip_html": html_tip,
        "plan_id": db_plan.id,
        "user_name": db_plan.owner.name 
    })

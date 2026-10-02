"""
backend/routes.py — FastAPI routes for FitBuddy.

Defines the web endpoints:
  GET  /          → Home page with the user form
  POST /generate  → Calls Gemini, saves to DB, redirects to result
  GET  /result/{id} → Result page showing the saved plan
  GET  /users     → All Users / History page
"""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import User, get_db
from backend.gemini_service import generate_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with the fitness-profile form."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate")
async def generate(
    name: str = Form(...),
    age: int = Form(...),
    fitness_goal: str = Form(...),
    workout_intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    """Generate a 7-day plan via Gemini, store it, and redirect to the result."""
    plan_text = generate_plan(name, age, fitness_goal, workout_intensity)

    user = User(
        name=name,
        age=age,
        fitness_goal=fitness_goal,
        workout_intensity=workout_intensity,
        plan=plan_text,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return RedirectResponse(url=f"/result/{user.id}", status_code=303)


@router.get("/result/{user_id}", response_class=HTMLResponse)
async def result(request: Request, user_id: int, db: Session = Depends(get_db)):
    """Display a previously generated plan for the given user ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("result.html", {"request": request, "user": user})


@router.get("/users", response_class=HTMLResponse)
async def all_users(request: Request, db: Session = Depends(get_db)):
    """Render the All Users / History page with every saved plan."""
    users = db.query(User).order_by(User.created_at.desc()).all()
    return templates.TemplateResponse("all_users.html", {"request": request, "users": users})

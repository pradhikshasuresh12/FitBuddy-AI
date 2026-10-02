"""
main.py — FitBuddy application entry point.

Initializes the FastAPI app, mounts static files, creates the database
on startup, and includes all routes from backend.routes.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import init_db
from backend.routes import router

app = FastAPI(title="FitBuddy – AI Fitness & Wellness Planner")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup_event():
    """Create the SQLite database and tables on first launch."""
    init_db()
    print("[FitBuddy] Database initialized.")


app.include_router(router)

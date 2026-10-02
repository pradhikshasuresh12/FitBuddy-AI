# FitBuddy – AI Fitness & Wellness Planner

A full-stack web application that generates personalized 7-day fitness and wellness plans using Google Gemini AI. Built as a college project with Python FastAPI, SQLite, and SQLAlchemy.

## Project Description

FitBuddy is an AI-powered fitness planning app designed for beginners. Users enter their name, age, fitness goal, and workout intensity, and the app generates a safe, beginner-friendly 7-day workout and wellness plan using the Google Gemini AI API. All plans are saved to a database and can be reviewed anytime through the All Users / History page.

## Features

- **Personalized AI Plans** — Generates a custom 7-day fitness and wellness plan tailored to the user's profile using Google Gemini.
- **User Profile Form** — Collects name, age, fitness goal, and workout intensity.
- **Plan History** — All generated plans are saved and viewable on the All Users page.
- **Responsive UI** — Clean green and dark theme that works on mobile, tablet, and desktop.
- **Auto Database Creation** — SQLite database is created automatically on first startup.
- **Safe Fallback** — If the Gemini API is unavailable, a default beginner plan is provided.
- **Environment-Based Config** — API keys are loaded from environment variables, never hardcoded.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript, Jinja2 templates |
| Backend | Python, FastAPI, Uvicorn |
| Database | SQLite, SQLAlchemy ORM |
| AI | Google Gemini API (`google-generativeai`) |
| Markdown Rendering | `marked.js` (CDN) |

## Architecture

```
Browser (User)
    │
    ▼
FastAPI (main.py)
    ├── Routes (backend/routes.py)    → Handles web pages and form submission
    ├── Gemini Service (backend/)      → Calls Google Gemini API for plan generation
    └── Database (database.py)         → SQLAlchemy + SQLite for persistence
         └── Templates (templates/)    → Jinja2 HTML rendering
         └── Static (static/)          → CSS, JS assets
```

**Request flow:**
1. User visits the home page and fills out the fitness profile form.
2. On submit, the backend calls the Gemini AI service to generate a 7-day plan.
3. The plan and user info are saved to the SQLite database.
4. The user is redirected to the result page showing the rendered plan.
5. All saved plans are accessible from the All Users / History page.

## Installation Steps

### Prerequisites
- Python 3.9 or higher
- A Google Gemini API key (see configuration below)

### 1. Clone or download the project
```bash
cd FitBuddy
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # On macOS/Linux
# OR
venv\Scripts\activate           # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key
```bash
cp .env.example .env
```
Then open `.env` and replace `your_gemini_api_key_here` with your actual Gemini API key.

### 5. Run the application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open in browser
Navigate to: **http://localhost:8000**

## How to Configure GEMINI_API_KEY

1. Go to [Google AI Studio](https://aistudio.google.com/apikey) and sign in with a Google account.
2. Click **Create API Key** and copy the generated key.
3. Open the `.env` file in the project root (create it by copying `.env.example`).
4. Set the key:
   ```
   GEMINI_API_KEY=AIzaSy...your_key_here...
   ```
5. Save the file. The app reads this automatically on startup.

> **Important:** Never commit your `.env` file. It is already in `.gitignore`.

## How to Run the Application

```bash
# Activate your virtual environment (if not already active)
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at **http://localhost:8000**.

- **Home page:** http://localhost:8000/
- **All Users:** http://localhost:8000/users

The SQLite database (`fitbuddy.db`) is created automatically in the project directory on first run.

## Project Folder Structure

```
FitBuddy/
├── backend/
│   ├── __init__.py
│   ├── gemini_service.py      # Google Gemini AI integration
│   └── routes.py              # FastAPI route handlers
├── static/
│   ├── css/
│   │   └── style.css          # Green & dark theme styles
│   └── js/
│       └── main.js            # Form + Markdown rendering logic
├── templates/
│   ├── base.html              # Shared layout (nav, footer)
│   ├── index.html             # Home page with user form
│   ├── result.html            # 7-day plan result page
│   └── all_users.html         # All Users / History page
├── database.py                # SQLAlchemy setup + User model
├── main.py                    # FastAPI app entry point
├── requirements.txt           # Python dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Files excluded from version control
└── README.md                  # This file
```

## Notes

- If `GEMINI_API_KEY` is not set or the API is unreachable, the app uses a built-in fallback plan so it still works for demonstrations.
- The app uses SQLite, which stores data in a single file (`fitbuddy.db`). No external database server is needed.
- All API keys and secrets are kept in environment variables and are never exposed in frontend code.

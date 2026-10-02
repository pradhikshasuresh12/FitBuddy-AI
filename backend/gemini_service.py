"""
backend/gemini_service.py — Google Gemini AI integration for FitBuddy.

Calls the Gemini API to generate a safe, beginner-friendly 7-day fitness
and wellness plan tailored to the user's profile. The API key is read
from the GEMINI_API_KEY environment variable and never hardcoded.
"""

import os
import re

import google.generativeai as genai

# Gemini model identifier — "flash" is fast and cost-effective
MODEL_NAME = "gemini-1.5-flash"

# Fallback plan used if the API key is missing or the call fails.
FALLBACK_PLAN = """\
## Day 1 — Light Cardio & Mobility
**Workout:** 20-minute brisk walk, 10-minute full-body stretch
**Wellness:** Drink 8 glasses of water. Sleep 7-8 hours.

## Day 2 — Upper Body Strength (Beginner)
**Workout:** Wall push-ups 3x10, dumbbell rows 3x10, plank hold 3x20s
**Wellness:** Eat a protein-rich breakfast. 5-minute morning meditation.

## Day 3 — Active Recovery
**Workout:** 30-minute yoga or light stretching routine
**Wellness:** Track your mood in a journal. Avoid sugary drinks.

## Day 4 — Lower Body Strength (Beginner)
**Workout:** Bodyweight squats 3x12, lunges 3x10 each leg, glute bridge 3x15
**Wellness:** Eat leafy greens with lunch. Take a 15-minute walk after dinner.

## Day 5 — Cardio Endurance
**Workout:** 25-minute jogging or cycling at moderate pace, 5-minute cooldown
**Wellness:** Practice deep breathing for 5 minutes. Hydrate well.

## Day 6 — Full Body Circuit
**Workout:** 3 rounds: 10 squats, 10 push-ups (modified if needed), 30s plank, 10 jumping jacks
**Wellness:** Meal-prep a healthy snack. Connect with a friend or family member.

## Day 7 — Rest & Reflect
**Workout:** Rest day. Optional 15-minute gentle walk or stretch.
**Wellness:** Review your week. Set one small goal for next week. Prioritize sleep.

---
*Note: This is a general beginner plan. Always consult a doctor before starting a new fitness routine.*
"""


def _build_prompt(name: str, age: int, fitness_goal: str, intensity: str) -> str:
    return (
        "You are FitBuddy, an AI fitness and wellness coach. Create a safe, "
        "beginner-friendly 7-day fitness and wellness plan for the following person.\n\n"
        f"Name: {name}\n"
        f"Age: {age}\n"
        f"Fitness Goal: {fitness_goal}\n"
        f"Workout Intensity: {intensity}\n\n"
        "Requirements:\n"
        "1. Cover exactly 7 days (Day 1 through Day 7).\n"
        "2. Each day should include a Workout section and a Wellness section.\n"
        "3. Use Markdown headings (##) for each day.\n"
        "4. Keep exercises safe and beginner-appropriate for the given intensity.\n"
        "5. Include hydration, nutrition, sleep, and mental-wellness tips.\n"
        "6. Include one rest or active-recovery day.\n"
        "7. End with a brief safety disclaimer.\n"
        "8. Do not ask follow-up questions — output only the plan.\n"
    )


def _format_response(text: str) -> str:
    """Strip stray Markdown code-fence wrappers if the model adds them."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:markdown)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)
    return cleaned.strip()


def generate_plan(name: str, age: int, fitness_goal: str, intensity: str) -> str:
    """
    Generate a 7-day fitness and wellness plan via Gemini.

    Returns the plan as Markdown text. If the API key is missing or the
    request fails, a safe fallback plan is returned so the app still works.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    prompt = _build_prompt(name, age, fitness_goal, intensity)

    if not api_key:
        print("[FitBuddy] GEMINI_API_KEY not set — using fallback plan.")
        return FALLBACK_PLAN

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        raw = response.text if response.text else FALLBACK_PLAN
        return _format_response(raw)
    except Exception as exc:
        print(f"[FitBuddy] Gemini API error: {exc} — using fallback plan.")
        return FALLBACK_PLAN

import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None

API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def demo_recommendations(budget: float, category: str, preference: str, goal: str):
    remaining = max(budget, 0)
    return {
        "source": "demo",
        "summary": f"Budget plan for {category} within ₹{budget:,.0f}.",
        "recommendations": [
            {
                "name": f"Option A – {preference.title()} choice",
                "estimated_price": round(remaining * 0.45, 2),
                "reason": "Balanced choice that leaves room for other needs."
            },
            {
                "name": f"Option B – Value {category.title()} choice",
                "estimated_price": round(remaining * 0.30, 2),
                "reason": "Lower-cost option suitable for a limited budget."
            },
            {
                "name": f"Option C – Premium {category.title()} choice",
                "estimated_price": round(remaining * 0.20, 2),
                "reason": "Higher-feature option while keeping part of the budget unused."
            }
        ],
        "tips": [
            "Compare prices before purchasing.",
            "Keep 10–20% of the budget as a safety margin.",
            f"Prioritize features related to your goal: {goal}."
        ]
    }


def generate_recommendations(budget: float, category: str, preference: str, goal: str):
    if not API_KEY or genai is None:
        return demo_recommendations(budget, category, preference, goal)

    prompt = f"""
You are PocketSmart AI, a budget and recommendation assistant.
User budget: ₹{budget}
Category: {category}
Preference: {preference}
Goal: {goal}

Create 3 realistic recommendation ideas that fit the budget.
Return ONLY valid JSON with this structure:
{{
  "summary": "short summary",
  "recommendations": [
    {{"name":"...", "estimated_price": 0, "reason":"..."}}
  ],
  "tips": ["...", "...", "..."]
}}
Do not invent exact live prices or claim live availability.
"""

    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        text = response.text.strip()

        # Remove accidental markdown fences.
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        import json
        data = json.loads(text)
        data["source"] = "gemini"
        return data
    except Exception:
        return demo_recommendations(budget, category, preference, goal)

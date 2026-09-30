# PocketSmart AI – Your Smart Budget & Recommendation Assistant

A beginner-friendly GenAI project built with FastAPI and a simple HTML/CSS/JavaScript frontend.

## Features
- Enter a budget, category, preferences, and shopping goal
- Generate budget-aware recommendations
- FastAPI REST backend
- Gemini API integration through the official Google GenAI SDK
- Works with a demo fallback when no API key is configured
- Clean responsive frontend

## Project structure
```text
PocketSmart_AI/
├── backend/
│   ├── main.py
│   ├── ai_service.py
│   └── __init__.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── .env.example
├── requirements.txt
└── README.md
```

## Run
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env`.
5. Add your Gemini API key to `.env` if available.
6. Run:
   `uvicorn backend.main:app --reload`
7. Open http://127.0.0.1:8000

The app includes a demo fallback, so it can still show recommendations without an API key.

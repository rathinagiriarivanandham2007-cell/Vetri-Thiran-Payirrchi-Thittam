from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .ai_service import generate_recommendations

app = FastAPI(
    title="PocketSmart AI",
    description="Smart budget and recommendation assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendationRequest(BaseModel):
    budget: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)
    preference: str = Field(default="value for money", max_length=200)
    goal: str = Field(default="best choice within my budget", max_length=300)


@app.get("/api/health")
def health():
    return {"status": "ok", "project": "PocketSmart AI"}


@app.post("/api/recommend")
def recommend(request: RecommendationRequest):
    return generate_recommendations(
        request.budget,
        request.category,
        request.preference,
        request.goal
    )


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

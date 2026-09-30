import os, json
from typing import Optional, List
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="PocketSmart AI")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class PlannerRequest(BaseModel):
    planner: str
    budget: float
    preferences: dict = {}

DEMO = {
    "home": [
        {"name":"LED Ceiling Light","category":"Lighting","price":1499,"platform":"Amazon","reason":"Energy-efficient and suitable for modern rooms."},
        {"name":"Ceiling Fan","category":"Fan","price":2299,"platform":"Amazon","reason":"Balanced option for everyday use."},
        {"name":"Compact Dining Table","category":"Dining","price":6999,"platform":"IKEA","reason":"Space-saving design for smaller homes."},
        {"name":"Storage Cabinet","category":"Storage","price":3999,"platform":"IKEA","reason":"Useful storage while keeping the room organized."}
    ],
    "party": [
        {"name":"Party Meal Package","category":"Catering","price":3499,"platform":"Swiggy","reason":"Convenient group meal option."},
        {"name":"Decoration Package","category":"Decoration","price":2499,"platform":"Demo Vendor","reason":"Simple decoration package for a small event."},
        {"name":"Event Stay","category":"Accommodation","price":2999,"platform":"OYO","reason":"Example stay allocation when accommodation is needed."}
    ],
    "jewelry": [
        {"name":"Minimal Gold-tone Necklace","category":"Necklace","price":1299,"platform":"Amazon","reason":"Simple style that can work with many outfits."},
        {"name":"Stud Earrings","category":"Earrings","price":799,"platform":"Flipkart","reason":"Lightweight option for an occasion."},
        {"name":"Bracelet Set","category":"Bracelet","price":999,"platform":"Amazon","reason":"Easy to pair with festive outfits."}
    ]
}

def fallback(req):
    items = DEMO.get(req.planner, [])
    chosen = []
    total = 0
    for x in items:
        if total + x["price"] <= req.budget:
            chosen.append(x)
            total += x["price"]
    return {
        "summary": f"Demo plan created within ₹{req.budget:,.0f}.",
        "allocated": {"recommended_spend": total, "remaining": max(req.budget-total, 0)},
        "recommendations": chosen,
        "note": "These are demo recommendations. Connect approved catalog/affiliate APIs for live inventory and prices."
    }

def gemini_result(req):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return fallback(req)
    try:
        from google import genai
        client = genai.Client(api_key=key)
        prompt = f"""
You are PocketSmart AI, a budget planning assistant.
Planner: {req.planner}
Budget in INR: {req.budget}
User preferences/context: {json.dumps(req.preferences)}
Create a practical budget plan. Do not invent live product prices or claim a vendor has stock.
Return JSON with:
summary (string),
allocated (object with category names and numeric INR allocations),
recommendations (array of objects with name, category, estimated_price, platform, reason),
note (string).
Use estimated/example prices unless live catalog data is supplied.
"""
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        result = fallback(req)
        result["note"] += f" AI fallback used: {type(e).__name__}."
        return result

@app.get("/", response_class=HTMLResponse)
async def home():
    return open("app/static/index.html", encoding="utf-8").read()

@app.post("/api/plan")
async def plan(req: PlannerRequest):
    if req.budget <= 0:
        return JSONResponse({"error":"Budget must be greater than 0."}, status_code=400)
    return gemini_result(req)

@app.post("/api/jewelry-image")
async def jewelry_image(file: Optional[UploadFile] = File(None)):
    if not file:
        return {"uploaded": False}
    return {"uploaded": True, "filename": file.filename, "message":"Image received. Connect a multimodal Gemini workflow for color/style analysis."}

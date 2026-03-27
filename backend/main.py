import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, Form
from backend.database import save_candidate, get_candidates
from backend.model import extract_text, calculate_score

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Hiring Backend Running (Fixed SaaS)"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), job_desc: str = Form(...)):
    content = await file.read()
    
    text = extract_text(content)

    score = calculate_score(text, job_desc)

    data = {
        "name": file.filename,
        "score": score
    }

    save_candidate(data)

    return {"score": score}

@app.get("/candidates/")
def read_candidates():
    return get_candidates()

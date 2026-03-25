import sys
import os

# Ensure the parent directory is in the Python path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, Form
from backend.database import save_candidate, get_candidates
from backend.model import extract_text, calculate_score

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Hiring Backend Running (SQLite Edition)"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), job_desc: str = Form(...)):
    # Safely extract bytes
    content = await file.read()
    
    # Process PDF into proper text instead of crashing binary
    text = extract_text(content)

    # Calculate match
    score = calculate_score(text, job_desc)

    data = {
        "name": file.filename,
        "score": score
    }

    # Save to SQLite DB smoothly
    save_candidate(data)

    return {"score": score}

@app.get("/candidates/")
def read_candidates():
    # Return directly via SQLite helper
    return get_candidates()

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, Form
from backend.database import save_candidate, get_candidates, update_status, search_candidates
from backend.model import extract_text, calculate_score
from backend.parser import extract_data
from backend.emailer import send_email

app = FastAPI()

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), job_desc: str = Form(...)):
    content = await file.read()
    text = extract_text(content)

    score = calculate_score(text, job_desc)
    data_extracted = extract_data(text)

    data = {
        "name": file.filename,
        "score": score,
        "skills": data_extracted["skills"],
        "status": "Applied"
    }

    save_candidate(data)
    
    if score > 80:
        send_email(
            "candidate@email.com",
            "Shortlisted",
            "Congratulations! You are shortlisted."
        )

    return {"score": score}

@app.get("/candidates/")
def read_candidates():
    return get_candidates()

@app.get("/search/")
def search(skill: str):
    return search_candidates(skill)

@app.post("/update-status/")
def update_status_endpoint(name: str = Form(...), status: str = Form(...)):
    update_status(name, status)
    return {"message": "Success"}

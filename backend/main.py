from fastapi import FastAPI, UploadFile, File, Form
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

# DB
client = MongoClient("YOUR_MONGODB_URL")
db = client["resume_db"]
collection = db["candidates"]

# Model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), job_desc: str = Form(...)):
    content = await file.read()
    text = content.decode(errors="ignore")

    emb1 = model.encode(text, convert_to_tensor=True)
    emb2 = model.encode(job_desc, convert_to_tensor=True)

    score = float(util.cos_sim(emb1, emb2)) * 100

    data = {
        "name": file.filename,
        "score": score
    }

    collection.insert_one(data)

    return {"score": score}


@app.get("/candidates/")
def get_candidates():
    data = list(collection.find({}, {"_id": 0}))
    return data

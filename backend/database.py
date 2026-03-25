from pymongo import MongoClient

client = MongoClient("YOUR_MONGODB_URL")
db = client["resume_db"]
collection = db["candidates"]

def save_candidate(data):
    collection.insert_one(data)

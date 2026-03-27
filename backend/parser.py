import spacy
import os

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    pass # Managed by Pip install prior to run

def extract_data(text):
    if 'nlp' not in globals():
        return {"skills": []}
        
    doc = nlp(text)

    skills = []
    keywords = ["python", "machine learning", "sql", "java", "aws", "react", "docker"]

    for token in doc:
        if token.text.lower() in keywords:
            skills.append(token.text.lower())

    return {
        "skills": list(set(skills))
    }

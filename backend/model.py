import PyPDF2
import io
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

def extract_text(file_bytes):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text() + " "
        return text
    except Exception as e:
        return ""

def calculate_score(resume_text, jd):
    if not resume_text or not jd:
        return 0.0
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(jd, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2)
    return float(score.item()) * 100

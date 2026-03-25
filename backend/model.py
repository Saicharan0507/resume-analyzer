import PyPDF2
import io
from sentence_transformers import SentenceTransformer, util

# Keep on CPU to avoid Streamlit Cloud crashes and ensure consistency
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

def extract_text(file_bytes):
    """Robust fallback: Converts raw uploaded PDF bytes into text via PyPDF2 instead of string decoding."""
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

    # Use item() to correctly extract single float from tensor
    score = util.cos_sim(emb1, emb2)
    return float(score.item()) * 100

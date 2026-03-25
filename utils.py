import PyPDF2
from sentence_transformers import SentenceTransformer, util

# Keep device to CPU for Streamlit Cloud deployment compatibility
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

def extract_text(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text() + " "
        return text
    except Exception as e:
        raise e

def calculate_match_bert(resume_text, job_desc):
    if not resume_text or not job_desc:
        return 0.0
    # Encode both texts
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(job_desc, convert_to_tensor=True)
    
    # Calculate cosine similarity
    score = util.cos_sim(emb1, emb2)
    
    # Return as percentage
    return round(float(score) * 100, 2)

def generate_suggestions(score, missing_skills):
    suggestions = []

    if score < 50:
        suggestions.append("Your resume needs major improvement for this role.")
    elif score < 75:
        suggestions.append("Your resume is moderately aligned. Improve key skills.")
    else:
        suggestions.append("Your resume is well aligned. Minor improvements suggested.")

    if len(missing_skills) > 0:
        suggestions.append(f"Add these important skills: {', '.join(missing_skills[:5])}")

    suggestions.append("Include more project-based experience.")
    suggestions.append("Use strong action words (Built, Developed, Designed).")

    return suggestions

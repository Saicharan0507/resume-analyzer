import streamlit as st
import pandas as pd
from utils import extract_text, calculate_match_bert, generate_suggestions, get_missing_skills

# Page Configuration
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("🚀 AI Resume Analyzer (BERT + NLP)")
st.markdown("Analyze your resumes against job descriptions, get scores, and smart suggestions!")

# Job Roles for Recommendation
job_roles = {
    "Data Scientist": "python machine learning data analysis statistics sql deep learning",
    "Web Developer": "html css javascript react nodejs express frontend backend",
    "AI Engineer": "deep learning pytorch tensorflow nlp computer vision llm",
    "Data Analyst": "excel sql tableau powerbi data visualization dashboard",
    "Backend Developer": "python java c++ go postgresql mongodb api docker backend"
}

def recommend_jobs(resume_text):
    scores = {}
    for role, desc in job_roles.items():
        scores[role] = calculate_match_bert(resume_text, desc)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Tabs for Single and Multiple Resume Comparisons
tab1, tab2 = st.tabs(["Single Resume Match", "Multiple Resume Ranking"])

with tab1:
    st.header("1-on-1 Resume vs Job Description")
    col1, col2 = st.columns(2)
    
    with col1:
        job_desc = st.text_area(
            "Paste Job Description Here", 
            value="Looking for a Python developer with machine learning, SQL, and data analysis skills.",
            height=300
        )
    
    with col2:
        uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", key="single")

    if st.button("Analyze Resume"):
        if uploaded_file is None:
            st.error("Please upload a resume")
        elif not job_desc.strip():
            st.error("Please enter job description")
        else:
            with st.spinner("Analyzing with BERT model..."):
                try:
                    resume_text = extract_text(uploaded_file)
                    if not resume_text.strip():
                        st.error("Could not extract text from the PDF. It might be an image-based PDF.")
                    else:
                        score = calculate_match_bert(resume_text, job_desc)
                        missing = get_missing_skills(resume_text, job_desc)
                        suggestions = generate_suggestions(score, missing)

                        st.subheader("📊 Match Results")
                        st.progress(int(score))

                        if score > 80:
                            st.success(f"Excellent Match: {score}% 🚀")
                        elif score > 60:
                            st.warning(f"Good Match: {score}% ⚠️")
                        else:
                            st.error(f"Low Match: {score}% ❌")

                        chart_data = pd.DataFrame({
                            'Category': ['Match', 'Gap'],
                            'Value': [score, max(0, 100 - score)]
                        })
                        st.bar_chart(chart_data.set_index('Category'))

                        st.subheader("❗ Missing Skills")
                        st.write(", ".join(missing[:10]) if missing else "None identified")

                        st.subheader("💡 Suggestions")
                        for s in suggestions:
                            st.write("- " + s)
                            
                        st.subheader("🎯 Recommended Roles (Based on Resume):")
                        recommendations = recommend_jobs(resume_text)
                        for role, r_score in recommendations[:3]:
                            st.write(f"**{role}** → {r_score}% match")

                except Exception as e:
                    st.error("Error processing resume")

with tab2:
    st.header("Rank Multiple Resumes")
    job_desc_multi = st.text_area("Paste Job Description Here", height=150, key="multi_job")
    uploaded_files = st.file_uploader("Upload Multiple Resumes (PDFs)", type="pdf", accept_multiple_files=True, key="multi")
    
    if st.button("Rank Resumes"):
        if uploaded_files and job_desc_multi:
            with st.spinner("Ranking resumes using BERT..."):
                results = []
                for file in uploaded_files:
                    try:
                        text = extract_text(file)
                        if text.strip():
                            score = calculate_match_bert(text, job_desc_multi)
                            results.append((file.name, score))
                    except Exception as e:
                        st.error(f"Error reading {file.name}")
                
                if results:
                    st.subheader("🏆 Ranking Results")
                    # Sort results
                    results.sort(key=lambda x: x[1], reverse=True)
                    
                    for name, score in results:
                        st.write(f"**{name}** → {score}%")
                        
                    # Highlight top candidate
                    st.success(f"🥇 Top Candidate: **{results[0][0]}** with {results[0][1]}%")
        else:
            st.warning("Please upload at least one resume and paste a job description.")

# Footer
st.markdown("---")
st.caption("Built by Sai Charan | AI Project")

import streamlit as st
import pandas as pd
from utils import extract_text, calculate_match_bert, generate_suggestions

# Page Configuration
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("🚀 AI Resume Analyzer (BERT-powered)")
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
        job_desc = st.text_area("Paste Job Description Here", height=300)
    
    with col2:
        uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", key="single")

    if st.button("Analyze Resume"):
        if job_desc:
            if uploaded_file is not None:
                with st.spinner("Analyzing with BERT model..."):
                    try:
                        resume_text = extract_text(uploaded_file)
                        if not resume_text.strip():
                            st.error("Could not extract text from the PDF. It might be an image-based PDF.")
                        else:
                            # 1. Calculate Score
                            score = calculate_match_bert(resume_text, job_desc)
                            
                            st.subheader("📊 Match Results")
                            
                            # Add Progress Bar
                            st.progress(int(score))
                            
                            # Add Color Grading
                            if score > 80:
                                st.success(f"Excellent Match: {score}% 🚀")
                            elif score > 60:
                                st.warning(f"Good Match: {score}% ⚠️")
                            else:
                                st.error(f"Poor Match: {score}% ❌")
                                
                            # Add Simple Chart
                            chart_data = pd.DataFrame({
                                'Category': ['Match', 'Gap'],
                                'Value': [score, max(0, 100 - score)]
                            })
                            st.bar_chart(chart_data.set_index('Category'))
                            
                            # 2. Missing Skills & Suggestions
                            # Simple keyword based extraction for missing skills
                            job_words = set([w.strip().lower() for w in job_desc.replace(',', ' ').replace('.', ' ').split() if len(w) > 4])
                            resume_words = set([w.strip().lower() for w in resume_text.replace(',', ' ').replace('.', ' ').split() if len(w) > 4])
                            missing_skills = list(job_words - resume_words)
                            
                            suggestions = generate_suggestions(score, missing_skills)
                            st.subheader("💡 Suggestions to Improve:")
                            for s in suggestions:
                                st.write("- " + s)
                                
                            # 3. Job Recommendations
                            st.subheader("🎯 Recommended Roles (Based on Resume):")
                            recommendations = recommend_jobs(resume_text)
                            for role, r_score in recommendations[:3]:
                                st.write(f"**{role}** → {r_score}% match")
                                
                    except Exception as e:
                        st.error("Error reading PDF")
            else:
                st.warning("Please upload a resume.")
        else:
            st.warning("Please paste a job description.")

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

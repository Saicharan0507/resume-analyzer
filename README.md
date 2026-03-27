# 🚀 AI Hiring OS
*Next-Gen AI-Powered Recruitment & ATS Platform*

**AI Hiring OS** is a full-stack SaaS Enterprise application that automates resume screening, ranks candidates using cutting-edge NLP, and provides a fully interactive recruiter dashboard to manage the hiring pipeline. Designed to reduce human screening time by 80%.

---

### 🌟 Core Capabilities
- **AI Resume Screening:** Instantly calculates the mathematical Contextual Cosine Similarity between a candidate's resume and a job description using `Sentence-Transformers`.
- **Bulk Ranking System:** Upload 100s of resumes at once. The engine will parse, score, and rank them instantaneously, explicitly flagging the "Top Candidate" for recruiters.
- **NLP Keyword Parsing:** Uses `Spacy (en_core_web_sm)` to intelligently extract highly specific technical skills (e.g., Python, AWS, React) out of raw binary PDF bytes.
- **Advanced Recruiter Dashboard:** Built entirely with Streamlit and Altair Graphing, featuring interactive Pipeline Funnel doughnut charts and live Score Distribution analytics.
- **Persistent Database:** A robust SQLite pipeline that permanently saves scores, statuses, and technical matches, allowing recruiters to push candidates iteratively through the interview series (Applied → Shortlisted → Selected).
- **Automated Workflows:** Built-in PDF Download generation and modular Automated Emailing capabilities.
- **Smart Analytics Search:** Find candidates deeply buried in your system by dynamically filtering technical skills!

---

### 🏗️ Modular Tech Stack
- **Backend Engine:** FastAPI, Python, SQLite, Uvicorn
- **Frontend Dashboard:** Streamlit, Pandas, Altair, Reportlab
- **AI / NLP Architecture:** HuggingFace `all-MiniLM-L6-v2`, advanced `Spacy`, strict `PyPDF2` data buffering.

---

### ⚡ Quickstart Setup (Local Environment)
This architecture is cleanly decoupled into a microservices pattern (Backend API + Frontend GUI).

**1. Start the Machine Learning API Server (Terminal 1):**
```powershell
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m uvicorn backend.main:app --port 10000 --reload
```

**2. Start the Hiring Dashboard (Terminal 2):**
```powershell
streamlit run frontend/app.py
```

*Default Sandbox Credentials:* Username: `admin` | Password: `1234`

---

*Built independently by Sai Charan* 🚀

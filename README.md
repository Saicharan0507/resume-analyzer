# AI Resume Analyzer

An AI-powered resume analyzer using BERT embeddings that evaluates resume-job alignment, identifies missing skills, and provides intelligent recommendations. The system also supports multi-resume ranking and job role prediction.

## Features
- **AI Resume Analyzer**: Compares resumes against job descriptions.
- **BERT-based NLP Model**: Uses `sentence-transformers` (`all-MiniLM-L6-v2`).
- **Smart Suggestions**: Highlights missing skills and gives actionable advice.
- **Multi-Resume Ranking**: Evaluates multiple candidates simultaneously.
- **Job Recommendations**: Recommends job roles based on candidate's skills.
- **Streamlit UI**: Includes progress bars, color grading, and comparison charts.

## Deployment on Streamlit Cloud (100% Free)
Follow these exact steps to deploy without errors:

1. **Upload Project to GitHub**
   - Go to [GitHub](https://github.com/) and click "New Repository".
   - Upload the following files: `app.py`, `utils.py`, `requirements.txt`.

2. **Deploy on Streamlit Community Cloud**
   - Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
   - Click "New App".
   - Connect your GitHub account.
   - Select your newly created repository.
   - Set the **Main file path** to `app.py`.

3. **Click DEPLOY 🚀**

*Note: The code gracefully handles PDF errors and safely configures the BERT model to run on the CPU (`device='cpu'`) to ensure compatibility with Streamlit Cloud's free tier environments.*

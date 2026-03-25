import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
            st.rerun() # Refresh to let user through
        else:
            st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- MAIN DASHBOARD ----------------
st.title("🚀 AI Hiring SaaS Platform")

tab1, tab2, tab3 = st.tabs(["📄 Single", "📊 Bulk Ranking", "📂 Database"])

# Backend is running locally on port 10000 
BACKEND_URL = "http://localhost:10000"

# -------- SINGLE --------
with tab1:
    jd = st.text_area("Job Description", value="Looking for a Python developer with machine learning, SQL, and data analysis skills.")

    file = st.file_uploader("Upload Resume", type=["pdf"])

    if st.button("Analyze"):
        if file and jd:
            with st.spinner("Connecting to FastAPI Backend..."):
                res = requests.post(
                    f"{BACKEND_URL}/analyze/",
                    files={"file": (file.name, file.getvalue(), "application/pdf")},
                    data={"job_desc": jd}
                )

                if res.status_code == 200:
                    score = res.json()["score"]

                    st.progress(int(score))
                    if score > 80:
                        st.success(f"Excellent Match: {score:.2f}% 🚀")
                    elif score > 60:
                        st.warning(f"Good Match: {score:.2f}% ⚠️")
                    else:
                        st.error(f"Low Match: {score:.2f}% ❌")
                else:
                    st.error("Backend failed. Make sure FastAPI is running on port 10000!")

# -------- BULK --------
with tab2:
    jd_bulk = st.text_area("Job Description", key="bulk", value="Looking for a Python developer with machine learning, SQL, and data analysis skills.")

    files = st.file_uploader("Upload Multiple", type=["pdf"], accept_multiple_files=True)

    if st.button("Run Ranking"):
        if files and jd_bulk:
            with st.spinner("Ranking all candidates..."):
                results = []

                for f in files:
                    res = requests.post(
                        f"{BACKEND_URL}/analyze/",
                        files={"file": (f.name, f.getvalue(), "application/pdf")},
                        data={"job_desc": jd_bulk}
                    )

                    if res.status_code == 200:
                        score = res.json()["score"]
                        results.append({
                            "Name": f.name,
                            "Score": round(score, 2)
                        })

                if results:
                    df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

                    st.subheader("🏆 Top Candidate")
                    st.write(df.iloc[0])

                    st.dataframe(df)
                    st.bar_chart(df.set_index("Name"))

                    # Download
                    csv = df.to_csv(index=False).encode()
                    st.download_button("Download Results", csv, "results.csv", "text/csv")
                else:
                    st.error("Failed to generate results from Backend.")

# -------- DATABASE --------
with tab3:
    st.subheader("📂 Stored Candidates")

    if st.button("Refresh Database"):
        try:
            res = requests.get(f"{BACKEND_URL}/candidates/")
            if res.status_code == 200:
                data = res.json()
                df = pd.DataFrame(data)

                if not df.empty:
                    df = df.sort_values(by="score", ascending=False)
                    st.dataframe(df)
                    st.bar_chart(df.set_index("name"))
                else:
                    st.info("Database is empty. Analyze some resumes first!")
            else:
                st.error("Could not fetch data.")
        except:
             st.error("Cannot connect to backend database.")

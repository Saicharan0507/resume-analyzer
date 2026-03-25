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
        else:
            st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- MAIN DASHBOARD ----------------
st.title("🚀 AI Hiring SaaS Platform")

tab1, tab2, tab3 = st.tabs(["📄 Single", "📊 Bulk Ranking", "📂 Database"])

BACKEND_URL = "https://your-backend-url"

# -------- SINGLE --------
with tab1:
    jd = st.text_area("Job Description")

    file = st.file_uploader("Upload Resume")

    if st.button("Analyze"):
        if file and jd:
            res = requests.post(
                f"{BACKEND_URL}/analyze/",
                files={"file": file},
                data={"job_desc": jd}
            )

            score = res.json()["score"]

            st.progress(int(score))
            st.success(f"Score: {score:.2f}%")

# -------- BULK --------
with tab2:
    jd = st.text_area("Job Description", key="bulk")

    files = st.file_uploader("Upload Multiple", accept_multiple_files=True)

    if st.button("Run Ranking"):
        results = []

        for file in files:
            res = requests.post(
                f"{BACKEND_URL}/analyze/",
                files={"file": file},
                data={"job_desc": jd}
            )

            score = res.json()["score"]

            results.append({
                "Name": file.name,
                "Score": round(score, 2)
            })

        df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

        st.subheader("🏆 Top Candidate")
        st.write(df.iloc[0])

        st.dataframe(df)
        st.bar_chart(df.set_index("Name"))

        # Download
        csv = df.to_csv(index=False).encode()
        st.download_button("Download Results", csv, "results.csv")

# -------- DATABASE --------
with tab3:
    st.subheader("📂 Stored Candidates")

    res = requests.get(f"{BACKEND_URL}/candidates/")
    data = res.json()

    df = pd.DataFrame(data)

    if not df.empty:
        df = df.sort_values(by="score", ascending=False)
        st.dataframe(df)
        st.bar_chart(df.set_index("name"))
    else:
        st.info("No data yet")

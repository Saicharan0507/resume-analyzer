import streamlit as st
import requests
import pandas as pd
import altair as alt
from reportlab.platypus import SimpleDocTemplate, Paragraph

st.set_page_config(page_title="AI Hiring OS", layout="wide")

# ------------------ DARK THEME ------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


FREE_LIMIT = 5

if "user" not in st.session_state:
    st.session_state.user = None
if "usage" not in st.session_state:
    st.session_state.usage = 0

def login():
    st.title("🚀 AI Hiring OS")

    st.markdown("""
    ### Next-Gen AI Recruitment Platform

    ✔ Screen resumes instantly  
    ✔ Rank top candidates automatically  
    ✔ Save hiring time by 80%  
    ✔ Built for modern recruiters  
    ---
    """)
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Invalid login")
            
    st.success("✅ Trusted by early users (beta version)")

if not st.session_state.user:
    login()
    st.stop()


if st.session_state.usage >= FREE_LIMIT:
    st.warning("Free limit reached. Upgrade to Pro 🚀")
    st.stop()

# ------------------ SIDEBAR ------------------
st.sidebar.title("🚀 AI Hiring OS")
st.sidebar.write(f"👤 User: {st.session_state.user}")
st.sidebar.write(f"📊 Usage: {st.session_state.usage}/{FREE_LIMIT}")

menu = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Single Analysis",
    "Bulk Ranking",
    "Database",
    "Search",
    "Pricing"
])

BACKEND_URL = "http://localhost:10000"

def generate_pdf(name, score):
    file = f"{name}_report.pdf"
    doc = SimpleDocTemplate(file)
    content = []
    content.append(Paragraph(f"Candidate: {name}", None))
    content.append(Paragraph(f"Score: {score}", None))
    doc.build(content)
    return file

# ------------------ DASHBOARD ------------------
if menu == "Dashboard":
    st.title("📊 Hiring Dashboard")
    try:
        res = requests.get(f"{BACKEND_URL}/candidates/")
        data = res.json()
        df = pd.DataFrame(data)

        if not df.empty:
            col1, col2, col3 = st.columns(3)

            col1.metric("👥 Total Candidates", len(df))
            col2.metric("📈 Avg Score", round(df["score"].mean(), 2))
            col3.metric("🏆 Top Score", round(df["score"].max(), 2))

            st.markdown("---")
            st.subheader("📈 Pipeline Analytics")
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown("**Candidate Match Scores**")
                score_chart = alt.Chart(df).mark_bar(color='#4CAF50').encode(
                    x=alt.X('name', title='Candidate', sort='-y'),
                    y=alt.Y('score', title='Match Score (%)'),
                    tooltip=['name', 'score', 'status']
                ).properties(height=350)
                st.altair_chart(score_chart, use_container_width=True)
                
            with chart_col2:
                st.markdown("**Hiring Funnel Status Distribution**")
                status_counts = df['status'].value_counts().reset_index()
                status_counts.columns = ['status', 'count']
                
                funnel_chart = alt.Chart(status_counts).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta(field="count", type="quantitative"),
                    color=alt.Color(field="status", type="nominal", scale=alt.Scale(scheme='category20b')),
                    tooltip=['status', 'count']
                ).properties(height=350)
                st.altair_chart(funnel_chart, use_container_width=True)

        else:
            st.info("No data available yet")
    except:
        st.error("Backend Server is Offline.")

    st.markdown("---")
    st.subheader("🤖 AI Hiring Assistant")

    user_input = st.text_input("Ask about candidates or hiring")

    if user_input:
        if "best candidate" in user_input.lower():
            try:
                res = requests.get(f"{BACKEND_URL}/candidates/")
                df = pd.DataFrame(res.json())
                top = df.sort_values(by="score", ascending=False).iloc[0]
                st.write(f"Top candidate is **{top['name']}** with **{top['score']}%**")
            except:
                pass
        else:
            st.write("Try asking: best candidate")


# ------------------ SINGLE ------------------
elif menu == "Single Analysis":
    st.title("📄 Resume Analysis")

    jd = st.text_area("Job Description", value="Looking for a Python developer with machine learning, SQL, and data analysis skills.")
    file = st.file_uploader("Upload Resume", type=["pdf"])

    if st.button("Analyze Resume"):
        if file and jd:
            st.session_state.usage += 1
            res = requests.post(
                f"{BACKEND_URL}/analyze/",
                files={"file": (file.name, file.getvalue(), "application/pdf")},
                data={"job_desc": jd}
            )
            if res.status_code == 200:
                score = res.json()["score"]
                st.progress(int(score))

                if score > 80:
                    st.success(f"🚀 Excellent Match: {score:.2f}%")
                elif score > 60:
                    st.warning(f"⚠️ Good Match: {score:.2f}%")
                else:
                    st.error(f"❌ Low Match: {score:.2f}%")

                pdf = generate_pdf("Candidate", score)
                with open(pdf, "rb") as f:
                    st.download_button("Download PDF", f, file_name=pdf)

# ------------------ BULK ------------------
elif menu == "Bulk Ranking":
    st.title("📊 Bulk Resume Ranking")

    jd = st.text_area("Job Description", key="bulk")

    files = st.file_uploader("Upload Multiple Resumes", accept_multiple_files=True, type=["pdf"])

    if st.button("Run Ranking"):
        if files:
            results = []
            for file in files:
                st.session_state.usage += 1
                res = requests.post(
                    f"{BACKEND_URL}/analyze/",
                    files={"file": (file.name, file.getvalue(), "application/pdf")},
                    data={"job_desc": jd}
                )
                if res.status_code == 200:
                    score = res.json()["score"]
                    results.append({
                        "Name": file.name,
                        "Score": round(score, 2)
                    })

            df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

            st.subheader("🏆 Top Candidate")
            st.success(df.iloc[0].to_dict())

            st.dataframe(df)
            st.bar_chart(df.set_index("Name"))

            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download Results", csv, "results.csv")

# ------------------ DATABASE ------------------
elif menu == "Database":
    st.title("📂 Candidate Database")
    try:
        res = requests.get(f"{BACKEND_URL}/candidates/")
        df = pd.DataFrame(res.json())

        if not df.empty:
            st.dataframe(df)

            st.subheader("📊 Score Insights")
            st.line_chart(df["score"])
            
            st.markdown("---")
            st.subheader("Hiring Pipeline Tracker")
            status = st.selectbox("Update Status", ["Applied", "Shortlisted", "Interview", "Selected"])
            cand_name = st.selectbox("Select Candidate to Update", df['name'].tolist())

            if st.button("Update"):
                requests.post(f"{BACKEND_URL}/update-status/", data={"name": cand_name, "status": status})
                st.success("Status Updated! Refresh Database to view.")
        else:
            st.info("No candidates yet")
    except:
        st.error("Backend Error")

# ------------------ SEARCH ------------------
elif menu == "Search":
    st.title("🔍 Candidate Search")

    skill = st.text_input("Search by Skill")

    if st.button("Search"):
        try:
            res = requests.get(f"{BACKEND_URL}/search/?skill={skill}")
            df = pd.DataFrame(res.json())

            if not df.empty:
                st.dataframe(df)
            else:
                st.warning("No matching candidates found")
        except:
            st.error("Backend Error")
            
# ------------------ PRICING ------------------
elif menu == "Pricing":
    st.markdown("""
    # 🚀 AI Hiring OS  

    ### Hire 10x Faster with AI  

    ✔ Instantly analyze resumes  
    ✔ Rank top candidates automatically  
    ✔ Reduce hiring time by 80%  

    ---

    ### 🔥 Why Use This?
    - No manual resume screening  
    - Smart AI-based ranking  
    - Works for startups & recruiters  

    ---
    """)
    st.title("💰 Pricing Plans")

    col1, col2 = st.columns(2)

    col1.subheader("Free Plan")
    col1.write("✔ 5 resume analyses/day")
    col1.write("✔ Basic scoring")

    col2.subheader("Pro Plan 🚀")
    col2.write("✔ Unlimited analysis")
    col2.write("✔ Bulk ranking")
    col2.write("✔ Dashboard + analytics")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("""
### 🚀 Features
- AI Resume Screening  
- Bulk Candidate Ranking  
- Hiring Dashboard  
- Smart Search  
""")
st.caption("Next-gen AI-powered recruitment platform")

import streamlit as st
from auth import sign_in, sign_up, sign_in_with_google
from ai_engine import generate_resume, analyze_resume, analyze_winning_resume
from database import save_resume, get_user_resumes
import pdfplumber

st.set_page_config(layout="wide")

st.title("🚀 AI Career OS")

menu = st.sidebar.selectbox("Menu", ["Login", "Resume Builder", "ATS Analyzer", "Winning Resume Lab"])

if menu == "Login":
    st.subheader("Login or Sign Up")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        sign_in(email, password)
        st.success("Logged in!")

    if st.button("Sign Up"):
        sign_up(email, password)
        st.success("Account created!")

    if st.button("Login with Google"):
        sign_in_with_google()


elif menu == "Resume Builder":
    st.subheader("Generate Resume")

    name = st.text_input("Full Name")
    education = st.text_area("Education")
    experience = st.text_area("Experience")
    skills = st.text_area("Skills")
    target_role = st.text_input("Target Role")
    job_description = st.text_area("Job Description")

    if st.button("Generate"):
        data = {
            "name": name,
            "email": "",
            "education": education,
            "experience": experience,
            "skills": skills,
            "target_role": target_role,
            "job_description": job_description
        }

        resume = generate_resume(data)
        st.text_area("Generated Resume", resume, height=400)

elif menu == "ATS Analyzer":
    st.subheader("Upload Resume for Analysis")

    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        result = analyze_resume(text)
        st.write(result)

elif menu == "Winning Resume Lab":
    st.subheader("Upload Winning Resume")

    file = st.file_uploader("Upload Winning Resume PDF", type=["pdf"])

    if file:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        result = analyze_winning_resume(text)
        st.write(result)

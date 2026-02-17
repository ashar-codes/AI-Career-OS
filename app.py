import streamlit as st
from auth import sign_in, sign_up, sign_in_with_google
from ai_engine import generate_resume, analyze_resume, analyze_winning_resume
from database import save_resume, get_user_resumes
import pdfplumber

st.set_page_config(layout="wide")

st.title("🚀 AI Career OS")

# -------------------------
# SESSION STATE
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Resume Builder", "ATS Analyzer", "Winning Resume Lab"]
)

# -------------------------
# LOGIN PAGE
# -------------------------
if menu == "Login":
    st.subheader("Login or Sign Up")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # LOGIN
    if st.button("Login"):
        try:
            response = sign_in(email, password)

            if response and response.user:
                st.session_state.user = response.user
                st.success("Logged in successfully!")
            else:
                st.error("Invalid email or password.")

        except Exception as e:
            st.error(f"Login error: {e}")

    # SIGNUP
    if st.button("Sign Up"):
        try:
            response = sign_up(email, password)

            if response and response.user:
                st.success("Account created! Check your email if verification is enabled.")
            else:
                st.error("Signup failed.")

        except Exception as e:
            st.error(f"Signup error: {e}")

    # GOOGLE LOGIN
    if st.button("Login with Google"):
        try:
            sign_in_with_google()
        except Exception as e:
            st.error(f"Google login error: {e}")

# -------------------------
# RESUME BUILDER
# -------------------------
elif menu == "Resume Builder":

    if not st.session_state.user:
        st.warning("Please login first.")
    else:
        st.subheader("Generate Resume")

        name = st.text_input("Full Name")
        education = st.text_area("Education")
        experience = st.text_area("Experience")
        skills = st.text_area("Skills")
        target_role = st.text_input("Target Role")
        job_description = st.text_area("Job Description")

        if st.button("Generate"):
            try:
                data = {
                    "name": name,
                    "email": st.session_state.user.email,
                    "education": education,
                    "experience": experience,
                    "skills": skills,
                    "target_role": target_role,
                    "job_description": job_description
                }

                resume = generate_resume(data)
                st.text_area("Generated Resume", resume, height=400)

            except Exception as e:
                st.error(f"Resume generation error: {e}")

# -------------------------
# ATS ANALYZER
# -------------------------
elif menu == "ATS Analyzer":

    if not st.session_state.user:
        st.warning("Please login first.")
    else:
        st.subheader("Upload Resume for Analysis")

        file = st.file_uploader("Upload PDF", type=["pdf"])

        if file:
            try:
                with pdfplumber.open(file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted

                result = analyze_resume(text)
                st.write(result)

            except Exception as e:
                st.error(f"Analysis error: {e}")

# -------------------------
# WINNING RESUME LAB
# -------------------------
elif menu == "Winning Resume Lab":

    if not st.session_state.user:
        st.warning("Please login first.")
    else:
        st.subheader("Upload Winning Resume")

        file = st.file_uploader("Upload Winning Resume PDF", type=["pdf"])

        if file:
            try:
                with pdfplumber.open(file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted

                result = analyze_winning_resume(text)
                st.write(result)

            except Exception as e:
                st.error(f"Winning resume analysis error: {e}")

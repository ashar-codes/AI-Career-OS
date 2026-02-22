import streamlit as st
import json
from auth import sign_in, sign_up, sign_in_with_google
from ai_engine import generate_resume, analyze_resume, analyze_winning_resume
from html_templates import bold_corporate_template
import pdfplumber

st.set_page_config(layout="wide")
st.title("🚀 AI Career OS")

# -------------------------
# SESSION STATE
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "resume_data" not in st.session_state:
    st.session_state.resume_data = None

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Resume Builder", "ATS Analyzer", "Winning Resume Lab"],
)

# =========================
# LOGIN PAGE
# =========================
if menu == "Login":

    st.subheader("Login or Sign Up")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

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

    if st.button("Sign Up"):
        try:
            response = sign_up(email, password)
            if response and response.user:
                st.success("Account created!")
            else:
                st.error("Signup failed.")
        except Exception as e:
            st.error(f"Signup error: {e}")

    if st.button("Login with Google"):
        try:
            sign_in_with_google()
        except Exception as e:
            st.error(f"Google login error: {e}")

# =========================
# RESUME BUILDER
# =========================
elif menu == "Resume Builder":

    if not st.session_state.user:
        st.warning("Please login first.")
    else:

        st.subheader("Generate Resume")

        name = st.text_input("Full Name")
        education = st.text_area("Education")
        experience = st.text_area("Experience")
        skills = st.text_area("Skills (comma separated)")
        target_role = st.text_input("Target Role")
        job_description = st.text_area("Job Description")

        if st.button("Generate Resume"):
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

                raw_output = generate_resume(data)
                resume_json = json.loads(raw_output)

                resume_json["name"] = name
                resume_json["email"] = st.session_state.user.email

                st.session_state.resume_data = resume_json
                st.success("Resume generated successfully!")

            except Exception as e:
                st.error(f"Resume generation error: {e}")

        # -------------------------
        # EDIT + PREVIEW
        # -------------------------
        if st.session_state.resume_data:

            resume = st.session_state.resume_data

            st.divider()
            st.subheader("✏ Edit Resume")

            resume["summary"] = st.text_area(
                "Professional Summary",
                resume.get("summary", "")
            )

            resume["education"] = st.text_area(
                "Education Section",
                resume.get("education", "")
            )

            skills_input = st.text_area(
                "Skills (comma separated)",
                ", ".join(resume.get("skills", []))
            )

            resume["skills"] = [
                s.strip() for s in skills_input.split(",") if s.strip()
            ]

            st.divider()
            st.subheader("🎨 Design Options")

            preset_colors = {
                "Corporate Blue": "#1f4e79",
                "Charcoal": "#333333",
                "Emerald": "#0f5132",
                "Burgundy": "#6f1d1b",
                "Navy": "#1a237e"
            }

            preset = st.selectbox("Preset Color", list(preset_colors.keys()))
            accent_color = st.color_picker(
                "Custom Accent Color",
                preset_colors[preset]
            )

            # Generate HTML
            html_preview = bold_corporate_template(resume, accent_color)

            st.divider()
            st.subheader("👀 Live Preview")

            st.components.v1.html(
                html_preview,
                height=900,
                scrolling=True
            )

            st.divider()

            st.download_button(
                label="⬇ Download Resume (HTML)",
                data=html_preview,
                file_name="resume.html",
                mime="text/html"
            )

            st.info(
                "Download → Open in browser → Press Ctrl+P (Cmd+P on Mac) → Save as PDF."
            )

# =========================
# ATS ANALYZER
# =========================
elif menu == "ATS Analyzer":

    if not st.session_state.user:
        st.warning("Please login first.")
    else:
        st.subheader("Upload Resume for Analysis")

        file = st.file_uploader("Upload PDF", type=["pdf"])

        if file:
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

            result = analyze_resume(text)
            st.write(result)

# =========================
# WINNING RESUME LAB
# =========================
elif menu == "Winning Resume Lab":

    if not st.session_state.user:
        st.warning("Please login first.")
    else:
        st.subheader("Upload Winning Resume")

        file = st.file_uploader("Upload Winning Resume PDF", type=["pdf"])

        if file:
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

            result = analyze_winning_resume(text)
            st.write(result)

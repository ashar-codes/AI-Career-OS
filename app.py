import streamlit as st
import json
from auth import sign_in, sign_up, sign_in_with_google
from ai_engine import generate_resume, analyze_resume, analyze_winning_resume
from html_templates import bold_corporate_template
from pdf_generator import generate_pdf_from_html
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
    key="main_menu"
)

# -------------------------
# LOGIN PAGE
# -------------------------
if menu == "Login":

    st.subheader("Login or Sign Up")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_btn"):
        try:
            response = sign_in(email, password)
            if response and response.user:
                st.session_state.user = response.user
                st.success("Logged in successfully!")
            else:
                st.error("Invalid email or password.")
        except Exception as e:
            st.error(f"Login error: {e}")

    if st.button("Sign Up", key="signup_btn"):
        try:
            response = sign_up(email, password)
            if response and response.user:
                st.success("Account created!")
            else:
                st.error("Signup failed.")
        except Exception as e:
            st.error(f"Signup error: {e}")

    if st.button("Login with Google", key="google_btn"):
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

        name = st.text_input("Full Name", key="name")
        education = st.text_area("Education", key="education")
        experience = st.text_area("Experience", key="experience")
        skills = st.text_area("Skills (comma separated)", key="skills")
        target_role = st.text_input("Target Role", key="target_role")
        job_description = st.text_area("Job Description", key="job_desc")

        if st.button("Generate Resume", key="generate_resume_btn"):

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
        # EDITABLE PREVIEW
        # -------------------------
        if st.session_state.resume_data:

            resume = st.session_state.resume_data

            st.divider()
            st.subheader("✏ Edit Resume")

            resume["summary"] = st.text_area(
                "Professional Summary",
                resume.get("summary", ""),
                key="summary_edit"
            )

            resume["education"] = st.text_area(
                "Education Section",
                resume.get("education", ""),
                key="education_edit"
            )

            skills_input = st.text_area(
                "Skills (comma separated)",
                ", ".join(resume.get("skills", [])),
                key="skills_edit"
            )

            resume["skills"] = [
                s.strip() for s in skills_input.split(",") if s.strip()
            ]

            st.markdown("### Experience")

            for i, exp in enumerate(resume.get("experience", [])):

                exp["title"] = st.text_input(
                    f"Title {i+1}",
                    exp.get("title", ""),
                    key=f"title_{i}"
                )

                exp["company"] = st.text_input(
                    f"Company {i+1}",
                    exp.get("company", ""),
                    key=f"company_{i}"
                )

                exp["duration"] = st.text_input(
                    f"Duration {i+1}",
                    exp.get("duration", ""),
                    key=f"duration_{i}"
                )

                bullets_text = st.text_area(
                    f"Bullets {i+1} (one per line)",
                    "\n".join(exp.get("bullets", [])),
                    key=f"bullets_{i}"
                )

                exp["bullets"] = [
                    b.strip() for b in bullets_text.split("\n") if b.strip()
                ]

            st.markdown("### Projects")

            for i, proj in enumerate(resume.get("projects", [])):

                proj["title"] = st.text_input(
                    f"Project Title {i+1}",
                    proj.get("title", ""),
                    key=f"proj_title_{i}"
                )

                proj_bullets = st.text_area(
                    f"Project Bullets {i+1} (one per line)",
                    "\n".join(proj.get("bullets", [])),
                    key=f"proj_bullets_{i}"
                )

                proj["bullets"] = [
                    b.strip() for b in proj_bullets.split("\n") if b.strip()
                ]

            # -------------------------
            # DESIGN OPTIONS
            # -------------------------
            st.divider()
            st.subheader("🎨 Design Options")

            preset_colors = {
                "Corporate Blue": "#1f4e79",
                "Charcoal": "#333333",
                "Emerald": "#0f5132",
                "Burgundy": "#6f1d1b",
                "Navy": "#1a237e"
            }

            preset = st.selectbox(
                "Preset Color",
                list(preset_colors.keys()),
                key="preset_select"
            )

            accent_color = st.color_picker(
                "Custom Accent Color",
                preset_colors[preset],
                key="color_picker"
            )

            st.divider()

        

          
# HTML PREVIEW
# -------------------------
html_preview = bold_corporate_template(resume, accent_color)

st.subheader("👀 Live Preview")
st.components.v1.html(html_preview, height=900, scrolling=True)

st.divider()

# -------------------------
# DOWNLOAD HTML
# -------------------------
st.download_button(
    label="⬇ Download Resume (HTML)",
    data=html_preview,
    file_name="resume.html",
    mime="text/html"
)

st.info("After downloading, open the file in your browser → Press Ctrl+P (Cmd+P on Mac) → Save as PDF.")

# -------------------------
# ATS ANALYZER
# -------------------------
elif menu == "ATS Analyzer":

    if not st.session_state.user:
        st.warning("Please login first.")
    else:
        st.subheader("Upload Resume for Analysis")

        file = st.file_uploader("Upload PDF", type=["pdf"], key="ats_upload")

        if file:
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

            result = analyze_resume(text)
            st.write(result)

# -------------------------
# WINNING RESUME LAB
# -------------------------
elif menu == "Winning Resume Lab":

    if not st.session_state.user:
        st.warning("Please login first.")
    else:
        st.subheader("Upload Winning Resume")

        file = st.file_uploader("Upload Winning Resume PDF", type=["pdf"], key="winning_upload")

        if file:
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

            result = analyze_winning_resume(text)
            st.write(result)

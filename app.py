import streamlit as st
import json
from auth import sign_in, sign_up, sign_in_with_google
from ai_engine import generate_resume, analyze_resume, analyze_winning_resume
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
    ["Login", "Resume Builder", "ATS Analyzer", "Winning Resume Lab"]
)

# -------------------------
# LOGIN PAGE
# -------------------------
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

# -------------------------
# RESUME BUILDER
# -------------------------
elif menu == "Resume Builder":

    import json
    from pdf_generator import generate_pdf

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

                raw_output = generate_resume(data)
                resume_json = json.loads(raw_output)

                # Ensure name is stored
                resume_json["name"] = name

                st.session_state.resume_data = resume_json

            except Exception as e:
                st.error(f"Resume generation error: {e}")

        # -------------------------
        # EDITABLE PREVIEW
        # -------------------------
        if st.session_state.resume_data:

            st.divider()
            st.subheader("✏ Edit Resume")

            resume = st.session_state.resume_data

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
            resume["skills"] = [s.strip() for s in skills_input.split(",") if s.strip()]

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

            template = st.selectbox(
                "Template",
                ["Corporate Minimal", "Modern Two Column", "Executive Elegant", "Creative Accent"],
                index=0
            )

            font_choice = st.selectbox(
                "Font",
                ["Helvetica", "Arial", "Open Sans", "Montserrat", "Georgia", "Times New Roman", "Roboto"],
                index=0
            )

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

            photo = st.file_uploader(
                "Upload Profile Picture (Optional)",
                type=["jpg", "png"]
            )

            # -------------------------
            # PDF GENERATION
            # -------------------------
            if st.button("Generate PDF"):

                pdf_path = generate_pdf(
                    resume,
                    template,
                    font_choice,
                    accent_color,
                    photo
                )

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📄 Download Resume PDF",
                        f,
                        file_name="resume.pdf",
                        mime="application/pdf"
                    )

        # -------------------------
        # EDITABLE PREVIEW
        # -------------------------
        if st.session_state.resume_data:

            st.divider()
            st.subheader("✏ Edit Resume")

            resume = st.session_state.resume_data

            resume["summary"] = st.text_area("Professional Summary", resume.get("summary", ""))

            resume["education"] = st.text_area("Education Section", resume.get("education", ""))

            skills_input = st.text_area(
                "Skills (comma separated)",
                ", ".join(resume.get("skills", []))
            )
            resume["skills"] = [s.strip() for s in skills_input.split(",") if s.strip()]

            st.markdown("### Experience")

            for i, exp in enumerate(resume.get("experience", [])):
                exp["title"] = st.text_input(f"Title {i+1}", exp.get("title", ""), key=f"title_{i}")
                exp["company"] = st.text_input(f"Company {i+1}", exp.get("company", ""), key=f"company_{i}")
                exp["duration"] = st.text_input(f"Duration {i+1}", exp.get("duration", ""), key=f"duration_{i}")

                bullets_text = st.text_area(
                    f"Bullets {i+1} (one per line)",
                    "\n".join(exp.get("bullets", [])),
                    key=f"bullets_{i}"
                )
                exp["bullets"] = [b.strip() for b in bullets_text.split("\n") if b.strip()]

            st.markdown("### Projects")

            for i, proj in enumerate(resume.get("projects", [])):
                proj["title"] = st.text_input(f"Project Title {i+1}", proj.get("title", ""), key=f"proj_title_{i}")

                proj_bullets = st.text_area(
                    f"Project Bullets {i+1} (one per line)",
                    "\n".join(proj.get("bullets", [])),
                    key=f"proj_bullets_{i}"
                )
                proj["bullets"] = [b.strip() for b in proj_bullets.split("\n") if b.strip()]

            # -------------------------
            # TEMPLATE & STYLE OPTIONS
            # -------------------------
            st.divider()
            st.subheader("🎨 Design Options")

            template = st.selectbox(
                "Template",
                ["Corporate Minimal", "Modern Two Column", "Executive Elegant", "Creative Accent"],
                index=0
            )

            font_choice = st.selectbox(
                "Font",
                ["Helvetica", "Arial", "Open Sans", "Montserrat", "Georgia", "Times New Roman", "Roboto"],
                index=0
            )

            preset_colors = {
                "Corporate Blue": "#1f4e79",
                "Charcoal": "#333333",
                "Emerald": "#0f5132",
                "Burgundy": "#6f1d1b",
                "Navy": "#1a237e"
            }

            preset = st.selectbox("Preset Color", list(preset_colors.keys()))
            accent_color = st.color_picker("Custom Accent Color", preset_colors[preset])

            photo = st.file_uploader("Upload Profile Picture (Optional)", type=["jpg", "png"])

            st.success("Resume ready for PDF generation (PDF engine coming next).")

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

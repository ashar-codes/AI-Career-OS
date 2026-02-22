import base64

def bold_corporate_template(resume, accent_color, photo):

    # ------------------ PROFILE IMAGE ------------------
    image_html = ""
    if photo:
        image_bytes = photo.read()
        encoded = base64.b64encode(image_bytes).decode()
        image_html = f"""
        <div class="profile-container">
            <img src="data:image/png;base64,{encoded}" class="profile-pic">
        </div>
        """

    # ------------------ SKILLS ------------------
    skills_html = ""
    for i, skill in enumerate(resume.get("skills", [])[:8]):
        width = 85 - (i * 5)  # dynamic variation
        skills_html += f"""
        <div class="skill">
            <div class="skill-name">{skill}</div>
            <div class="skill-bar">
                <div class="skill-fill" style="width:{width}%;"></div>
            </div>
        </div>
        """

    # ------------------ EXPERIENCE ------------------
    experience_html = ""
    for exp in resume.get("experience", []):
        bullets = "".join([f"<li>{b}</li>" for b in exp.get("bullets", [])])
        experience_html += f"""
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
                <div class="job-title">{exp.get("title","")} <span class="company">| {exp.get("company","")}</span></div>
                <ul>{bullets}</ul>
            </div>
        </div>
        """

    html = f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <style>

        @page {{
            size: A4;
            margin: 0;
        }}

        body {{
            margin: 0;
            font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
            background: #ffffff;
            -webkit-font-smoothing: antialiased;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
        }}

        /* ================= HEADER ================= */
        .header {{
            background: linear-gradient(90deg, #1f1f1f, #2e2e2e);
            color: white;
            padding: 60px 40px 50px 40px;
            text-align: center;
            position: relative;
        }}

        .header h1 {{
            margin: 0;
            font-size: 42px;
            font-weight: 700;
            letter-spacing: 1px;
        }}

        .subtitle {{
            margin-top: 10px;
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #bbbbbb;
        }}

        .divider {{
            width: 70px;
            height: 4px;
            background: {accent_color};
            margin: 22px auto 0;
            border-radius: 3px;
        }}

        /* ================= PROFILE ================= */
        .profile-container {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            bottom: -55px;
        }}

        .profile-pic {{
            width: 110px;
            height: 110px;
            border-radius: 50%;
            border: 5px solid white;
            object-fit: cover;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}

        /* ================= LAYOUT ================= */
        .container {{
            display: flex;
            margin-top: 70px;
        }}

        .sidebar {{
            width: 30%;
            background: #2f2f2f;
            color: #f5f5f5;
            padding: 45px 35px;
        }}

        .content {{
            width: 70%;
            padding: 60px 60px;
            background: #ffffff;
        }}

        /* ================= SECTION HEADERS ================= */
        h2 {{
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-weight: 600;
            border-bottom: 2px solid {accent_color};
            padding-bottom: 6px;
            margin-top: 35px;
        }}

        p {{
            font-size: 14px;
            line-height: 1.7;
            margin-top: 10px;
        }}

        /* ================= SKILLS ================= */
        .skill {{
            margin-bottom: 18px;
        }}

        .skill-name {{
            font-size: 13px;
            margin-bottom: 6px;
        }}

        .skill-bar {{
            background: #444;
            height: 6px;
            border-radius: 6px;
        }}

        .skill-fill {{
            height: 6px;
            background: {accent_color};
            border-radius: 6px;
        }}

        /* ================= TIMELINE ================= */
        .timeline {{
            position: relative;
            padding-left: 30px;
        }}

        .timeline::before {{
            content: '';
            position: absolute;
            left: 8px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: {accent_color};
        }}

        .timeline-item {{
            position: relative;
            margin-bottom: 35px;
        }}

        .timeline-dot {{
            position: absolute;
            left: -2px;
            top: 6px;
            width: 12px;
            height: 12px;
            background: {accent_color};
            border-radius: 50%;
        }}

        .job-title {{
            font-weight: 600;
            font-size: 16px;
        }}

        .company {{
            color: {accent_color};
            font-weight: 500;
        }}

        ul {{
            margin-top: 10px;
            padding-left: 18px;
        }}

        li {{
            font-size: 14px;
            margin-bottom: 8px;
            line-height: 1.6;
        }}

        .education-text {{
            font-size: 13px;
            line-height: 1.6;
            margin-top: 10px;
        }}

    </style>
    </head>

    <body>
    <div class="page">

        <div class="header">
            <h1>{resume.get("name","")}</h1>
            <div class="subtitle">Software Engineer</div>
            <div class="divider"></div>
            {image_html}
        </div>

        <div class="container">

            <div class="sidebar">
                <h2>✉ Contact</h2>
                <p>{resume.get("email","")}</p>

                <h2>⚙ Skills</h2>
                {skills_html}

                <h2>🎓 Education</h2>
                <div class="education-text">
                    {resume.get("education","")}
                </div>
            </div>

            <div class="content">

                <h2>🧠 Summary</h2>
                <p>{resume.get("summary","")}</p>

                <h2>💼 Experience</h2>
                <div class="timeline">
                    {experience_html}
                </div>

            </div>

        </div>

    </div>
    </body>
    </html>
    """

    return html

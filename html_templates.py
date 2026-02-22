import base64

def bold_corporate_template(resume, accent_color, photo):

    image_html = ""
    if photo:
        image_bytes = photo.read()
        encoded = base64.b64encode(image_bytes).decode()
        image_html = f"""
        <div class="profile-wrapper">
            <img src="data:image/png;base64,{encoded}" class="profile-pic">
        </div>
        """

    skills_html = ""
    for i, skill in enumerate(resume.get("skills", [])[:8]):
        width = 90 - (i * 6)
        skills_html += f"""
        <div class="skill">
            <div class="skill-name">{skill}</div>
            <div class="skill-bar">
                <div class="skill-fill" style="width:{width}%"></div>
            </div>
        </div>
        """

    experience_html = ""
    for exp in resume.get("experience", []):
        bullets = "".join([f"<li>{b}</li>" for b in exp.get("bullets", [])])
        experience_html += f"""
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
                <div class="job-title">
                    {exp.get("title","")}
                    <span class="company">| {exp.get("company","")}</span>
                </div>
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
            font-family: 'Inter', 'Segoe UI', sans-serif;
            background: #f4f6f8;
            -webkit-font-smoothing: antialiased;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
            margin: auto;
            background: white;
            box-shadow: 0 20px 60px rgba(0,0,0,0.08);
        }}

        /* ================= HEADER ================= */
        .header {{
            background: linear-gradient(120deg, #1c1c1c, #2b2b2b);
            color: white;
            padding: 70px 40px 60px 40px;
            text-align: center;
            position: relative;
        }}

        .header h1 {{
            margin: 0;
            font-size: 44px;
            font-weight: 700;
            letter-spacing: 1px;
        }}

        .subtitle {{
            margin-top: 10px;
            font-size: 14px;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #bbbbbb;
        }}

        .accent-line {{
            width: 80px;
            height: 4px;
            background: {accent_color};
            margin: 25px auto 0;
            border-radius: 3px;
            box-shadow: 0 0 10px {accent_color};
        }}

        /* ================= PROFILE ================= */
        .profile-wrapper {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            bottom: -60px;
        }}

        .profile-pic {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 6px solid white;
            object-fit: cover;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}

        /* ================= LAYOUT ================= */
        .container {{
            display: flex;
            margin-top: 90px;
        }}

        .sidebar {{
            width: 30%;
            background: #262626;
            color: #f1f1f1;
            padding: 50px 35px;
        }}

        .content {{
            width: 70%;
            padding: 70px 65px;
            background: #ffffff;
        }}

        /* ================= TYPOGRAPHY ================= */
        h2 {{
            font-size: 13px;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-weight: 600;
            border-bottom: 2px solid {accent_color};
            padding-bottom: 6px;
            margin-top: 40px;
        }}

        p {{
            font-size: 14px;
            line-height: 1.8;
            color: #333;
        }}

        /* ================= SKILLS ================= */
        .skill {{
            margin-bottom: 20px;
        }}

        .skill-name {{
            font-size: 13px;
            margin-bottom: 6px;
        }}

        .skill-bar {{
            background: #3d3d3d;
            height: 6px;
            border-radius: 6px;
        }}

        .skill-fill {{
            height: 6px;
            background: {accent_color};
            border-radius: 6px;
            box-shadow: 0 0 8px {accent_color};
        }}

        /* ================= TIMELINE ================= */
        .timeline {{
            position: relative;
            padding-left: 35px;
        }}

        .timeline::before {{
            content: '';
            position: absolute;
            left: 10px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: {accent_color};
            opacity: 0.5;
        }}

        .timeline-item {{
            position: relative;
            margin-bottom: 40px;
        }}

        .timeline-dot {{
            position: absolute;
            left: 4px;
            top: 6px;
            width: 10px;
            height: 10px;
            background: {accent_color};
            border-radius: 50%;
            box-shadow: 0 0 8px {accent_color};
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
            line-height: 1.7;
            color: #333;
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
            <div class="accent-line"></div>
            {image_html}
        </div>

        <div class="container">

            <div class="sidebar">
                <h2>Contact</h2>
                <p>{resume.get("email","")}</p>

                <h2>Skills</h2>
                {skills_html}

                <h2>Education</h2>
                <div class="education-text">
                    {resume.get("education","")}
                </div>
            </div>

            <div class="content">

                <h2>Summary</h2>
                <p>{resume.get("summary","")}</p>

                <h2>Experience</h2>
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

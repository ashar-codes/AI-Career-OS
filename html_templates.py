def bold_corporate_template(resume, accent_color):

    skills_html = ""
    for skill in resume.get("skills", [])[:8]:
        skills_html += f"""
        <div class="skill">
            <div class="skill-name">{skill}</div>
            <div class="skill-bar">
                <div class="skill-fill"></div>
            </div>
        </div>
        """

    experience_html = ""
    for exp in resume.get("experience", []):
        bullets = "".join([f"<li>{b}</li>" for b in exp.get("bullets", [])])
        experience_html += f"""
        <div class="experience-item">
            <div class="job-title">{exp.get("title","")} <span class="company">| {exp.get("company","")}</span></div>
            <ul>{bullets}</ul>
        </div>
        """

    html = f"""
    <html>
    <head>
    <style>

        @page {{
            size: A4;
            margin: 0;
        }}

        body {{
            margin: 0;
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
        }}

        /* HEADER */
        .header {{
            background: linear-gradient(90deg, #111111, #1e1e1e);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}

        .header h1 {{
            margin: 0;
            font-size: 38px;
            letter-spacing: 1px;
            font-weight: 700;
        }}

        .divider {{
            width: 60px;
            height: 4px;
            background: {accent_color};
            margin: 18px auto 0;
        }}

        /* MAIN LAYOUT */
        .container {{
            display: flex;
        }}

        .sidebar {{
            width: 32%;
            background: #151515;
            color: white;
            padding: 40px 30px;
        }}

        .content {{
            width: 68%;
            background: #f7f7f7;
            padding: 50px 45px;
        }}

        /* SECTION HEADERS */
        h2 {{
            font-size: 16px;
            letter-spacing: 2px;
            font-weight: 600;
            text-transform: uppercase;
            border-bottom: 2px solid {accent_color};
            padding-bottom: 6px;
            margin-top: 30px;
        }}

        /* TEXT */
        p {{
            font-size: 14px;
            line-height: 1.6;
        }}

        ul {{
            padding-left: 18px;
            margin-top: 8px;
        }}

        li {{
            font-size: 14px;
            margin-bottom: 6px;
            line-height: 1.5;
        }}

        /* JOB TITLE */
        .job-title {{
            font-weight: 600;
            font-size: 15px;
            margin-top: 18px;
        }}

        .company {{
            color: {accent_color};
            font-weight: 500;
        }}

        /* SKILLS */
        .skill {{
            margin-bottom: 16px;
        }}

        .skill-name {{
            font-size: 13px;
            margin-bottom: 6px;
        }}

        .skill-bar {{
            background: #333;
            height: 4px;
        }}

        .skill-fill {{
            width: 70%;
            height: 4px;
            background: {accent_color};
        }}

        /* EDUCATION */
        .education-text {{
            font-size: 13px;
            line-height: 1.5;
        }}

    </style>
    </head>

    <body>
    <div class="page">

        <div class="header">
            <h1>{resume.get("name","")}</h1>
            <div class="divider"></div>
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
                {experience_html}

            </div>

        </div>

    </div>
    </body>
    </html>
    """

    return html

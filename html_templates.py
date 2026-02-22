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
            font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
            background: #ffffff;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
        }}

        /* HEADER */
        .header {{
            background: linear-gradient(90deg, #2a2a2a, #1f1f1f);
            color: white;
            padding: 55px 40px 45px 40px;
            text-align: center;
        }}

        .header h1 {{
            margin: 0;
            font-size: 40px;
            font-weight: 700;
            letter-spacing: 1px;
        }}

        .subtitle {{
            margin-top: 10px;
            font-size: 15px;
            letter-spacing: 2px;
            color: #cccccc;
            text-transform: uppercase;
        }}

        .divider {{
            width: 70px;
            height: 4px;
            background: {accent_color};
            margin: 22px auto 0;
            border-radius: 4px;
        }}

        /* MAIN LAYOUT */
        .container {{
            display: flex;
        }}

        .sidebar {{
            width: 30%;
            background: #2f2f2f;
            color: #f0f0f0;
            padding: 45px 35px;
        }}

        .content {{
            width: 70%;
            background: #ffffff;
            padding: 55px 50px;
        }}

        /* SECTION HEADERS */
        h2 {{
            font-size: 15px;
            letter-spacing: 2px;
            font-weight: 600;
            text-transform: uppercase;
            border-bottom: 2px solid {accent_color};
            padding-bottom: 6px;
            margin-top: 35px;
        }}

        /* TEXT */
        p {{
            font-size: 14px;
            line-height: 1.7;
            margin-top: 10px;
        }}

        ul {{
            padding-left: 18px;
            margin-top: 8px;
        }}

        li {{
            font-size: 14px;
            margin-bottom: 8px;
            line-height: 1.6;
        }}

        /* JOB TITLE */
        .job-title {{
            font-weight: 600;
            font-size: 15px;
            margin-top: 25px;
        }}

        .company {{
            color: {accent_color};
            font-weight: 500;
        }}

        /* SKILLS */
        .skill {{
            margin-bottom: 18px;
        }}

        .skill-name {{
            font-size: 13px;
            margin-bottom: 6px;
        }}

        .skill-bar {{
            background: #444;
            height: 5px;
            border-radius: 6px;
        }}

        .skill-fill {{
            width: 70%;
            height: 5px;
            background: {accent_color};
            border-radius: 6px;
        }}

        /* EDUCATION */
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
            <div class="subtitle">Junior Software Engineer</div>
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

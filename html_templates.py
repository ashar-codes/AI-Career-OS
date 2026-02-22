def bold_corporate_template(resume, accent_color):

    skills_html = ""
    for skill in resume.get("skills", [])[:6]:
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
            <h4>{exp.get("title","")} | {exp.get("company","")}</h4>
            <ul>{bullets}</ul>
        </div>
        """

    html = f"""
    <html>
    <head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}

        .header {{
            background: #1f1f1f;
            color: white;
            text-align: center;
            padding: 40px;
            font-size: 32px;
            font-weight: bold;
        }}

        .container {{
            display: flex;
        }}

        .sidebar {{
            width: 33%;
            background: #2a2a2a;
            color: white;
            padding: 30px;
        }}

        .content {{
            width: 67%;
            background: #f4f4f4;
            padding: 40px;
        }}

        h3 {{
            border-bottom: 2px solid {accent_color};
            padding-bottom: 5px;
        }}

        .skill-bar {{
            background: #555;
            height: 6px;
            margin-top: 5px;
            margin-bottom: 15px;
        }}

        .skill-fill {{
            background: {accent_color};
            width: 70%;
            height: 6px;
        }}

        ul {{
            padding-left: 20px;
        }}
    </style>
    </head>

    <body>

    <div class="header">
        {resume.get("name","")}
    </div>

    <div class="container">
        <div class="sidebar">
            <h3>Contact</h3>
            <p>{resume.get("email","")}</p>

            <h3>Skills</h3>
            {skills_html}

            <h3>Education</h3>
            <p>{resume.get("education","")}</p>
        </div>

        <div class="content">
            <h3>Summary</h3>
            <p>{resume.get("summary","")}</p>

            <h3>Experience</h3>
            {experience_html}
        </div>
    </div>

    </body>
    </html>
    """

    return html

import base64

def bold_corporate_template(resume, accent_color, photo):

    # Convert uploaded image to base64
    image_html = ""
    if photo:
        image_bytes = photo.read()
        encoded = base64.b64encode(image_bytes).decode()
        image_html = f"""
        <div class="profile-container">
            <img src="data:image/png;base64,{encoded}" class="profile-pic">
        </div>
        """

    # Skills
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

    # Experience timeline
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
    <style>

        @page {{
            size: A4;
            margin: 0;
        }}

        body {{
            margin: 0;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
        }}

        /* HEADER */
        .header {{
            background: linear-gradient(90deg, #2a2a2a, #1f1f1f);
            color: white;
            padding: 50px;
            text-align: center;
            position: relative;
        }}

        .header h1 {{
            margin: 0;
            font-size: 38px;
            font-weight: 700;
        }}

        .divider {{
            width: 60px;
            height: 4px;
            background: {accent_color};
            margin: 18px auto;
            border-radius: 3px;
        }}

        /* Profile */
        .profile-container {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            bottom: -50px;
        }}

        .profile-pic {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 5px solid white;
            object-fit: cover;
        }}

        /* Layout */
        .container {{
            display: flex;
            margin-top: 60px;
        }}

        .sidebar {{
            width: 30%;
            background: #2f2f2f;
            color: white;
            padding: 40px 30px;
        }}

        .content {{
            width: 70%;
            padding: 50px;
            background: #ffffff;
        }}

        h2 {{
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            border-bottom: 2px solid {accent_color};
            padding-bottom: 6px;
            margin-top: 30px;
        }}

        p {{
            font-size: 14px;
            line-height: 1.6;
        }}

        /* Skills */
        .skill {{
            margin-bottom: 15px;
        }}

        .skill-name {{
            font-size: 13px;
        }}

        .skill-bar {{
            height: 4px;
            background: #444;
            border-radius: 4px;
            margin-top: 5px;
        }}

        .skill-fill {{
            height: 4px;
            width: 70%;
            background: {accent_color};
            border-radius: 4px;
        }}

        /* Timeline */
        .timeline-item {{
            position: relative;
            margin-left: 20px;
            margin-bottom: 30px;
        }}

        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -20px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: {accent_color};
        }}

        .timeline-dot {{
            width: 10px;
            height: 10px;
            background: {accent_color};
            border-radius: 50%;
            position: absolute;
            left: -25px;
            top: 5px;
        }}

        .job-title {{
            font-weight: 600;
            font-size: 15px;
        }}

        .company {{
            color: {accent_color};
        }}

        ul {{
            margin-top: 8px;
        }}

        li {{
            margin-bottom: 6px;
            font-size: 14px;
        }}

    </style>
    </head>

    <body>
    <div class="page">

        <div class="header">
            <h1>{resume.get("name","")}</h1>
            <div class="divider"></div>
            {image_html}
        </div>

        <div class="container">

            <div class="sidebar">
                <h2>Contact</h2>
                <p>{resume.get("email","")}</p>

                <h2>Skills</h2>
                {skills_html}

                <h2>Education</h2>
                <p>{resume.get("education","")}</p>
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

from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"


# -------------------------
# RESUME GENERATION (JSON)
# -------------------------
def generate_resume(data):

    prompt = f"""
You are a professional resume writer.

Generate a resume in STRICT JSON format.

Return ONLY valid JSON.
No explanation.
No markdown.
No extra text.

Format exactly like this:

{{
  "summary": "",
  "education": "",
  "skills": [],
  "experience": [
    {{
      "title": "",
      "company": "",
      "duration": "",
      "bullets": []
    }}
  ],
  "projects": [
    {{
      "title": "",
      "bullets": []
    }}
  ]
}}

Candidate Information:
Name: {data['name']}
Email: {data['email']}
Education: {data['education']}
Experience: {data['experience']}
Skills: {data['skills']}
Target Role: {data['target_role']}
Job Description: {data['job_description']}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1500
    )

    output = response.choices[0].message.content.strip()

    # Safety: Ensure valid JSON
    try:
        json.loads(output)
    except:
        raise ValueError("AI returned invalid JSON format.")

    return output


# -------------------------
# ATS ANALYZER
# -------------------------
def analyze_resume(text):

    prompt = f"""
Analyze this resume.

Provide:
- ATS score (0-100)
- Strengths
- Weaknesses
- Improvement suggestions

Resume:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()


# -------------------------
# WINNING RESUME ANALYZER
# -------------------------
def analyze_winning_resume(text):

    prompt = f"""
This is a high-quality winning resume.

Explain:
- Why it is strong
- Structural advantages
- Bullet style patterns
- Keyword strategy
- What makes it recruiter-friendly

Resume:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()

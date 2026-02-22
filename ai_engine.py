from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_resume(data):

    prompt = f"""
You are an expert ATS resume writer.

IMPORTANT:
- Do NOT include explanations.
- Do NOT include reasoning.
- Do NOT include <think> tags.
- Output ONLY the final formatted resume.
- No commentary.
- No notes.
- No formatting instructions.

Create a clean, professional, ATS-optimized resume.

Use:
- Strong action verbs
- Quantified impact where possible
- Clear section headings
- Single-column format
- No extra commentary

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
    messages=[
        {"role": "system", "content": "You generate professional resumes only. No reasoning. No explanations."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.4,
)

    return response.choices[0].message.content


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
   model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content


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
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content

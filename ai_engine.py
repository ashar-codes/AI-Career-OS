from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"

MODEL = "openai/gpt-oss-120b"

def generate_resume(data):

    prompt = f"""
Create a professional ATS-optimized resume.

Output ONLY the final resume.
Do NOT include explanations.
Do NOT include reasoning.
Start directly with the candidate name.

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
        temperature=0.3,
        max_tokens=1200
    )

    return response.choices[0].message.content.strip()


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
   MODEL = "openai/gpt-oss-120b",
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
        MODEL = "openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content

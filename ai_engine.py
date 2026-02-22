from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "qwen/qwen3-32b"

def generate_resume(data):

    prompt = f"""
Generate a professional ATS-optimized resume.

STRICT RULES:
- Output ONLY the resume.
- No explanations.
- No reasoning.
- No notes.
- No commentary.
- Do NOT include <think>.
- Do NOT describe your thinking.
- Do NOT include formatting notes.
- Start directly with the candidate name.

Format:
Name
Contact
Professional Summary
Education
Technical Skills
Professional Experience
Projects (if applicable)

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
            {
                "role": "system",
                "content": "You are a resume generator. You NEVER output reasoning. You NEVER output analysis. You ONLY output the final resume."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1500
    )

    output = response.choices[0].message.content

    # Hard safety filter (production safety)
    if "<think>" in output:
        output = output.split("<think>")[-1]

    return output.strip()


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

from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_resume(data):

    prompt = f"""
    You are an expert ATS resume writer.

    Create a professional, achievement-focused resume.

    Candidate Information:
    Name: {data['name']}
    Email: {data['email']}
    Education: {data['education']}
    Experience: {data['experience']}
    Skills: {data['skills']}
    Target Role: {data['target_role']}
    Job Description: {data['job_description']}

    Requirements:
    - Use strong action verbs
    - Quantify impact
    - Optimize for ATS
    - Clean formatting
    """

    response = client.chat.completions.create(
model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
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
   model="llama-3.3-70b-versatile",
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
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content

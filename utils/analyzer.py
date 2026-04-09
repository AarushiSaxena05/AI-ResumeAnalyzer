import spacy
import os

nlp = spacy.load("en_core_web_sm")

# Extended skill database
SKILLS_DB = [
    "python", "java", "c++", "javascript", "typescript",
    "machine learning", "deep learning", "nlp",
    "sql", "mongodb", "postgresql",
    "html", "css", "react", "angular", "node.js",
    "aws", "azure", "gcp", "docker", "kubernetes",
    "data analysis", "pandas", "numpy", "matplotlib",
    "flask", "django", "fastapi",
    "git", "github", "linux"
]


def extract_keywords(text):
    doc = nlp(text)
    keywords = set()

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            keywords.add(token.text.lower())

    return list(keywords)


def match_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS_DB if skill in text]


def generate_feedback(resume, job_desc, missing_skills, score):
    try:
        import openai

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("No API key")

        openai.api_key = api_key

        prompt = f"""
        Resume Score: {score}%
        Missing Skills: {missing_skills}

        Resume:
        {resume[:1500]}

        Job Description:
        {job_desc[:1500]}

        Give:
        1. Improvement suggestions
        2. ATS optimization tips
        3. Strong actionable advice
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["choices"][0]["message"]["content"]

    except:
        # Fallback feedback (IMPORTANT for stability)
        feedback = f"""
🔍 Resume Analysis Summary:

✔ Match Score: {score}%

❌ Missing Skills:
{", ".join(missing_skills) if missing_skills else "None"}

📌 Suggestions:
- Add measurable achievements (e.g., increased performance by X%)
- Include relevant technical keywords
- Improve formatting (clear headings, bullet points)
- Align experience with job description
- Add projects related to required skills

🚀 ATS Tips:
- Use standard section headings (Skills, Experience, Projects)
- Avoid images or fancy graphics
- Keep resume concise (1–2 pages)
"""
        return feedback.strip()
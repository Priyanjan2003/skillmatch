import pdfplumber
import docx
import os
import re


def clean_text(text):
    """
    Lowercase, remove special characters, extra spaces
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return clean_text(text)


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = " ".join([para.text for para in doc.paragraphs])
    return clean_text(text)


def extract_resume_text(resume_path):
    """
    Detect file type and extract text
    """
    if not resume_path:
        return ""

    ext = os.path.splitext(resume_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(resume_path)
    elif ext == ".docx":
        return extract_text_from_docx(resume_path)

    return ""
def calculate_ats_score(resume_text, job):
    if not resume_text:
        return 0

    resume_words = set(resume_text.split())

    # -----------------------------
    # Build job text SAFELY
    # -----------------------------
    job_text_parts = []

    # Job title
    if hasattr(job, 'title'):
        job_text_parts.append(job.title)

    # Required skills
    job_skills = [skill.name for skill in job.required_skills.all()]
    job_text_parts.extend(job_skills)

    job_text = clean_text(" ".join(job_text_parts))
    job_words = set(job_text.split())

    # -----------------------------
    # ATS SCORE CALCULATION
    # -----------------------------

    # Skill match (60%)
    matched_skills = sum(
        1 for skill in job_skills if skill.lower() in resume_words
    )
    skill_score = (matched_skills / len(job_skills)) * 60 if job_skills else 0

    # Keyword match (40%)
    keyword_match = len(resume_words & job_words)
    keyword_score = min((keyword_match / max(len(job_words), 1)) * 40, 40)

    return round(skill_score + keyword_score, 2)

import PyPDF2
import docx
import re

# Common technical skills list
COMMON_SKILLS = [
    "python", "java", "c++", "sql", "machine learning",
    "deep learning", "data science", "html", "css",
    "javascript", "react", "node.js", "aws", "docker",
    "kubernetes", "git", "github", "tensorflow", "pandas",
    "numpy", "excel", "power bi", "tableau"
]


def extract_text_from_pdf(file_path):
    text = ""

    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            text += page.extract_text() + "\n"

    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


def extract_education(text):
    education_keywords = [
        "b.tech", "b.e", "m.tech", "mca",
        "bsc", "msc", "b.com", "mba", "phd"
    ]

    text = text.lower()

    for keyword in education_keywords:
        if keyword in text:
            return keyword.upper()

    return "Not Found"


def extract_experience(text):
    experience_keywords = [
        "internship",
        "experience",
        "worked at",
        "project"
    ]

    count = 0
    text = text.lower()

    for keyword in experience_keywords:
        count += text.count(keyword)

    return count


def parse_resume(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)

    else:
        return {
            "error": "Unsupported file format"
        }

    parsed_data = {
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_score": extract_experience(text),
        "raw_text": text
    }

    return parsed_data
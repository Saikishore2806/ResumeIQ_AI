import re

ROLE_SKILLS = {
    "data scientist": [
        "python", "sql", "machine learning",
        "pandas", "numpy", "tableau",
        "docker", "aws"
    ],

    "frontend developer": [
        "html", "css", "javascript",
        "react", "git", "github"
    ],

    "backend developer": [
        "python", "sql", "node.js",
        "docker", "aws", "git"
    ],

    "ml engineer": [
        "python", "machine learning",
        "deep learning", "tensorflow",
        "docker", "aws"
    ]
}


def calculate_ats_score(raw_text):
    ats_score = 0
    text = raw_text.lower()

    # Email Check
    if re.search(r'\S+@\S+', raw_text):
        ats_score += 5

    # Phone Number Check
    if re.search(r'\+?\d[\d\s-]{8,}', raw_text):
        ats_score += 5

    # LinkedIn Check
    if "linkedin" in text:
        ats_score += 5

    # GitHub Check
    if "github" in text:
        ats_score += 5

    # Education Section
    if "education" in text:
        ats_score += 5

    # Projects Section
    if "project" in text:
        ats_score += 5

    # Experience Section
    if "experience" in text or "internship" in text:
        ats_score += 5

    return min(ats_score, 25)


def score_resume(parsed_data, target_role="data scientist"):
    score = 0

    resume_skills = parsed_data.get("skills", [])
    required_skills = ROLE_SKILLS.get(
        target_role.lower(),
        ROLE_SKILLS["data scientist"]
    )

    # Skills Match Score (MAX 50)
    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_required = len(required_skills)

    if total_required > 0:
        skills_score = int((len(matched_skills) / total_required) * 50)
    else:
        skills_score = 0

    score += skills_score

    # Education Score (MAX 15)
    education = parsed_data.get("education", "")

    if education != "Not Found":
        education_score = 15
    else:
        education_score = 5

    score += education_score

    # Experience Score (MAX 15)
    experience = parsed_data.get("experience_score", 0)
    experience_score = min(experience * 5, 15)
    score += experience_score

    # Resume Length Score (MAX 10)
    raw_text = parsed_data.get("raw_text", "")
    word_count = len(raw_text.split())

    if word_count >= 300:
        length_score = 10
    elif word_count >= 150:
        length_score = 7
    else:
        length_score = 4

    score += length_score

    # ATS Score (MAX 10)
    ats_score = min(calculate_ats_score(raw_text), 10)
    score += ats_score

    final_result = {
        "Target Role": target_role,
        "Matched Skills": matched_skills,
        "Missing Skills": missing_skills,
        "Skills Score": skills_score,
        "Education Score": education_score,
        "Experience Score": experience_score,
        "Length Score": length_score,
        "ATS Score": ats_score,
        "Final Resume Score": score
    }

    return final_result
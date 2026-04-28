def generate_feedback(parsed_data, score_data):
    feedback = []

    target_role = score_data.get("Target Role", "")
    missing_skills = score_data.get("Missing Skills", [])
    final_score = score_data.get("Final Resume Score", 0)

    # Missing Skills Feedback
    if missing_skills:
        feedback.append(
            f"For the role of {target_role}, consider adding these skills: "
            + ", ".join(missing_skills)
        )

    # Score-based Feedback
    if final_score < 70:
        feedback.append(
            "Your resume needs stronger ATS optimization and better project descriptions."
        )

    elif final_score < 85:
        feedback.append(
            "Your resume is good, but adding measurable achievements and certifications will improve recruiter visibility."
        )

    else:
        feedback.append(
            "Your resume is strong and well-structured. Minor improvements can make it even better."
        )

    # Project Suggestion
    if score_data.get("Experience Score", 0) < 10:
        feedback.append(
            "Include more internships, live projects, or practical experience."
        )

    return feedback
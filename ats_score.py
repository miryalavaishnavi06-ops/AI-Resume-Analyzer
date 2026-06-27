DEFAULT_REQUIRED_SKILLS = [
        "Python",
        "Sql",
        "Machine Learning",
        "Power Bi",
        "Azure",
        "Git",
        "Docker",
        "Excel"
    ]


def calculate_ats_score(extracted_skills, required_skills=None):
    required_skills = required_skills or DEFAULT_REQUIRED_SKILLS

    matched = []

    missing = []

    for skill in required_skills:

        if skill in extracted_skills:
            matched.append(skill)

        else:
            missing.append(skill)

    if not required_skills:
        return 0, []

    score = (len(matched) / len(required_skills)) * 100

    return score, missing

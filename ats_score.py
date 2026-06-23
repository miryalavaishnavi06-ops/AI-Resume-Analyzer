def calculate_ats_score(extracted_skills):

    required_skills = [
        "Python",
        "Sql",
        "Machine Learning",
        "Power Bi",
        "Azure",
        "Git",
        "Docker",
        "Excel"
    ]

    matched = []

    missing = []

    for skill in required_skills:

        if skill in extracted_skills:
            matched.append(skill)

        else:
            missing.append(skill)

    score = (len(matched) / len(required_skills)) * 100

    return score, missing
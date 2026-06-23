def recommend_roles(skills):

    roles = []
    skills = {skill.lower() for skill in skills}

    role_rules = {
        "AI/ML Engineer": {"python", "machine learning"},
        "Data Analyst": {"sql", "pandas"},
        "Python Developer": {"python", "sql"},
        "Computer Vision Engineer": {"deep learning", "computer vision"},
        "Data Scientist": {"python", "scikit-learn"},
        "Frontend Developer": {"html", "css", "javascript"},
        "React Developer": {"react", "javascript"},
        "Backend Developer": {"python", "api"},
        "Full Stack Developer": {"react", "node.js"},
        "Cloud Engineer": {"aws", "azure"},
        "DevOps Engineer": {"docker", "kubernetes"},
        "Business Intelligence Analyst": {"power bi", "sql"},
        "Data Engineer": {"python", "sql", "aws"},
    }

    for role, required_skills in role_rules.items():
        if required_skills.issubset(skills):
            roles.append(role)

    return roles

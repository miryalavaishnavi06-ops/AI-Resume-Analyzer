def extract_skills(text):

    skill_list = [
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "html",
        "css",
        "react",
        "node.js",
        "express",
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "nlp",
        "cnn",
        "computer vision",
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "tensorflow",
        "keras",
        "pytorch",
        "git",
        "github",
        "power bi",
        "tableau",
        "excel",
        "azure",
        "aws",
        "gcp",
        "docker",
        "kubernetes",
        "linux",
        "api",
        "rest api",
        "flask",
        "django",
        "streamlit",
        "statistics",
        "data analysis",
        "data visualization"
    ]

    found_skills = []

    text = text.lower()

    for skill in skill_list:
        if skill in text:
            found_skills.append(skill.title())

    return found_skills

import re


SKILL_ALIASES = {
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "html": ["html"],
    "css": ["css"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular"],
    "vue": ["vue", "vue.js", "vuejs"],
    "node.js": ["node.js", "nodejs", "node"],
    "express": ["express", "express.js"],
    "spring boot": ["spring boot", "springboot"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo db"],
    "oracle": ["oracle"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision"],
    "numpy": ["numpy"],
    "pandas": ["pandas"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "keras": ["keras"],
    "pytorch": ["pytorch"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "excel": ["excel", "ms excel", "microsoft excel"],
    "statistics": ["statistics", "statistical analysis"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "visualization"],
    "git": ["git"],
    "github": ["github"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "linux": ["linux"],
    "api": ["api", "apis"],
    "rest api": ["rest api", "restful api"],
    "flask": ["flask"],
    "django": ["django"],
    "streamlit": ["streamlit"],
    "figma": ["figma"],
    "ui/ux": ["ui/ux", "ui ux", "user experience", "user interface"],
    "wireframing": ["wireframing", "wireframe"],
    "prototyping": ["prototyping", "prototype"],
    "adobe photoshop": ["adobe photoshop", "photoshop"],
    "adobe illustrator": ["adobe illustrator", "illustrator"],
    "seo": ["seo", "search engine optimization"],
    "digital marketing": ["digital marketing"],
    "content writing": ["content writing", "content creation"],
    "social media marketing": ["social media marketing"],
    "google analytics": ["google analytics"],
    "salesforce": ["salesforce"],
    "crm": ["crm", "customer relationship management"],
    "lead generation": ["lead generation"],
    "sales": ["sales"],
    "customer service": ["customer service", "customer support"],
    "accounting": ["accounting"],
    "financial analysis": ["financial analysis"],
    "tally": ["tally"],
    "quickbooks": ["quickbooks"],
    "gst": ["gst"],
    "recruitment": ["recruitment", "recruiting", "talent acquisition"],
    "hr": ["hr", "human resources"],
    "employee engagement": ["employee engagement"],
    "payroll": ["payroll"],
    "project management": ["project management"],
    "agile": ["agile"],
    "scrum": ["scrum"],
    "jira": ["jira"],
    "communication": ["communication", "communication skills"],
    "leadership": ["leadership"],
    "problem solving": ["problem solving", "problem-solving"],
    "stakeholder management": ["stakeholder management"],
    "cybersecurity": ["cybersecurity", "cyber security"],
    "network security": ["network security"],
    "penetration testing": ["penetration testing", "pentesting"],
    "siem": ["siem"],
}


def normalize_skill_name(skill):
    return skill.strip().title()


def contains_phrase(text, phrase):
    escaped = re.escape(phrase.lower())
    pattern = rf"(?<![a-z0-9+#]){escaped}(?![a-z0-9+#])"
    return re.search(pattern, text) is not None


def extract_skills(text):
    found_skills = []
    text = text.lower()

    for skill, aliases in SKILL_ALIASES.items():
        if any(contains_phrase(text, alias) for alias in aliases):
            found_skills.append(normalize_skill_name(skill))

    return found_skills

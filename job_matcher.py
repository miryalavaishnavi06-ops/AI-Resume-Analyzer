import re

from skills import extract_skills


STOPWORDS = {
    "about",
    "across",
    "after",
    "also",
    "and",
    "any",
    "are",
    "based",
    "be",
    "best",
    "business",
    "can",
    "candidate",
    "company",
    "degree",
    "department",
    "detail",
    "education",
    "etc",
    "excellent",
    "executive",
    "experience",
    "for",
    "from",
    "good",
    "have",
    "in",
    "including",
    "is",
    "job",
    "knowledge",
    "looking",
    "minimum",
    "must",
    "of",
    "on",
    "or",
    "our",
    "preferred",
    "related",
    "required",
    "requirements",
    "responsibilities",
    "role",
    "should",
    "skills",
    "strong",
    "team",
    "the",
    "this",
    "to",
    "tools",
    "using",
    "with",
    "work",
    "year",
    "years",
    "you",
}


def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_keywords(text, max_keywords=20):
    text = normalize_text(text)
    words = re.findall(r"[a-z][a-z0-9+#.-]*", text)
    words = [word for word in words if len(word) > 2 and word not in STOPWORDS]

    keywords = []
    for word in words:
        if word not in keywords:
            keywords.append(word)

    return keywords[:max_keywords]


def phrase_exists(text, phrase):
    pattern = rf"(?<![a-z0-9+#]){re.escape(phrase.lower())}(?![a-z0-9+#])"
    return re.search(pattern, normalize_text(text)) is not None


def match_resume_to_job(resume_text, job_description):
    if not job_description.strip():
        return None

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    jd_keywords = extract_keywords(job_description)

    resume_keywords = {
        keyword.title()
        for keyword in jd_keywords
        if phrase_exists(resume_text, keyword)
    }
    missing_keywords = {
        keyword.title()
        for keyword in jd_keywords
        if not phrase_exists(resume_text, keyword)
    }

    matched_skills = sorted(resume_skills.intersection(job_skills))
    missing_skills = sorted(job_skills.difference(resume_skills))

    if not job_skills and not jd_keywords:
        return {
            "match_score": 0,
            "skill_score": 0,
            "keyword_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "job_skills": [],
            "matched_keywords": [],
            "missing_keywords": [],
            "priority_gaps": [],
            "message": "No clear requirements were detected in the job description.",
        }

    skill_score = round((len(matched_skills) / len(job_skills)) * 100) if job_skills else 0
    keyword_score = round((len(resume_keywords) / len(jd_keywords)) * 100) if jd_keywords else 0

    if job_skills and jd_keywords:
        match_score = round((skill_score * 0.75) + (keyword_score * 0.25))
    elif job_skills:
        match_score = skill_score
    else:
        match_score = keyword_score

    priority_gaps = missing_skills[:5]
    for keyword in sorted(missing_keywords):
        if len(priority_gaps) >= 8:
            break
        if keyword not in priority_gaps:
            priority_gaps.append(keyword)

    return {
        "match_score": match_score,
        "skill_score": skill_score,
        "keyword_score": keyword_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "job_skills": sorted(job_skills),
        "matched_keywords": sorted(resume_keywords),
        "missing_keywords": sorted(missing_keywords),
        "priority_gaps": priority_gaps,
        "message": None,
    }

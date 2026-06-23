from skills import extract_skills


def match_resume_to_job(resume_text, job_description):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    if not job_description.strip():
        return None

    if not job_skills:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "job_skills": [],
            "message": "No known technical skills were detected in the job description.",
        }

    matched_skills = sorted(resume_skills.intersection(job_skills))
    missing_skills = sorted(job_skills.difference(resume_skills))
    match_score = round((len(matched_skills) / len(job_skills)) * 100)

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "job_skills": sorted(job_skills),
        "message": None,
    }

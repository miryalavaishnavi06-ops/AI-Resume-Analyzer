import os
import hashlib

import pandas as pd

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib"))

import matplotlib.pyplot as plt
import streamlit as st

from ats_score import calculate_ats_score
from gemini_helper import extract_resume_text_with_gemini, get_resume_feedback
from job_matcher import match_resume_to_job
from pdf_parser import extract_text_from_pdf
from pdf_report import build_pdf_report
from recommendation import recommend_roles
from skills import extract_skills


def show_resume_strength(score, is_jd_based=False):
    target = "this job" if is_jd_based else "a general resume check"

    if score >= 80:
        st.success(f"Strong match for {target}.")
    elif score >= 60:
        st.warning(f"Good start. A few improvements can make it stronger for {target}.")
    else:
        st.error(f"Needs work. Add more relevant skills and experience for {target}.")


def show_skill_chart(skills, missing_skills):
    coverage_data = pd.DataFrame(
        {
            "Category": ["Matched Skills", "Missing Skills"],
            "Count": [len(skills), len(missing_skills)],
        }
    )
    st.bar_chart(coverage_data, x="Category", y="Count", color="#2563eb")

    fig, ax = plt.subplots()
    sizes = [len(skills), len(missing_skills)]
    labels = ["Matched Skills", "Missing Skills"]
    colors = ["#2563eb", "#f97316"]

    if sum(sizes) > 0:
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors)
        ax.set_title("Skills Breakdown")
        st.pyplot(fig)
    else:
        st.info("Skill breakdown will appear after skills are detected.")

    plt.close(fig)


def show_skill_list(title, items, empty_message):
    st.subheader(title)
    if items:
        st.write(", ".join(items))
    else:
        st.info(empty_message)


def show_improvement_plan(job_match):
    priority_gaps = job_match.get("priority_gaps", [])

    if not priority_gaps:
        st.success("No major JD gaps detected. Focus on adding measurable achievements.")
        return

    st.subheader("What To Improve")
    st.write("Focus on these first:")
    for gap in priority_gaps:
        st.write(f"- {gap}")

    st.info(
        "Tip: Do not add fake skills. Add only the skills, tools, and responsibilities "
        "you can explain in an interview."
    )


def build_report(score_label, score, skills, general_missing_skills, recommended_roles, job_match, feedback):
    is_jd_based = job_match is not None and not job_match["message"]

    return f"""AI Resume Analysis Report

Score Type: {score_label}
Score: {score:.0f}%
Skills Found: {", ".join(skills) if skills else "None"}
General Checklist Gaps: {", ".join(general_missing_skills) if general_missing_skills else "None"}
Recommended Roles: {", ".join(recommended_roles) if recommended_roles else "None"}
JD Match: {"Not provided" if job_match is None else str(job_match["match_score"]) + "%"}
Skill Match: {"Not provided" if not is_jd_based else str(job_match["skill_score"]) + "%"}
Keyword Match: {"Not provided" if not is_jd_based else str(job_match["keyword_score"]) + "%"}
Priority Gaps: {"Not provided" if not is_jd_based else ", ".join(job_match["priority_gaps"]) or "None"}

AI Feedback:
{feedback}
"""


st.set_page_config(page_title="AI Resume Analyzer", page_icon=":page_facing_up:", layout="wide")

with st.sidebar:
    st.title("AI Resume Analyzer")
    st.write("Check how well a resume fits a job description.")
    st.markdown("---")
    st.write("How to use:")
    st.write("1. Upload resume PDF")
    st.write("2. Paste job description")
    st.write("3. Review match score and gaps")

st.title("AI Resume Analyzer")
st.caption("Upload a resume and paste a job description to see match score, gaps, and AI suggestions.")

input_col, jd_col = st.columns([1, 1])
with input_col:
    uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
with jd_col:
    job_description = st.text_area(
        "Paste Job Description",
        height=140,
        placeholder="Paste the target job description here...",
    )

if not uploaded_file:
    st.info("Upload a resume PDF to start the analysis.")
else:
    text = extract_text_from_pdf(uploaded_file)

    if len(text.strip()) < 100:
        st.warning(
            "This looks like a scanned or image-based resume. Trying Gemini text extraction..."
        )
        with st.spinner("Reading scanned PDF with Gemini..."):
            gemini_text = extract_resume_text_with_gemini(uploaded_file)

        if gemini_text.startswith("Error:"):
            st.error(gemini_text)
            st.stop()

        text = gemini_text
        st.success("Scanned resume text extracted successfully.")

    skills = extract_skills(text)
    general_score, general_missing_skills = calculate_ats_score(skills)
    recommended_roles = recommend_roles(skills)
    job_match = match_resume_to_job(text, job_description)
    is_jd_based = job_match is not None and not job_match["message"]
    score = job_match["match_score"] if is_jd_based else general_score
    score_label = "Job Match Score" if is_jd_based else "Resume Score"
    gap_count = (
        len(job_match["missing_skills"]) + len(job_match["missing_keywords"])
        if is_jd_based
        else len(general_missing_skills)
    )

    st.success("Resume uploaded successfully.")

    summary_cols = st.columns(4)
    summary_cols[0].metric(score_label, f"{score:.0f}%")
    summary_cols[1].metric("Skills Found", len(skills))
    summary_cols[2].metric("Gaps Found", gap_count)
    summary_cols[3].metric("Suggested Roles", len(recommended_roles))

    st.progress(int(score))
    show_resume_strength(score, is_jd_based)

    if job_match is None:
        st.info("Paste a job description to get a job-specific match score and missing requirements.")
    else:
        if job_match["message"]:
            st.info(job_match["message"])
        else:
            match_col, gap_col = st.columns(2)
            with match_col:
                show_skill_list(
                    "What Matches",
                    job_match["matched_skills"],
                    "No matching skills found yet.",
                )
            with gap_col:
                show_skill_list(
                    "Missing Skills",
                    job_match["missing_skills"],
                    "No missing skills detected.",
                )

            show_improvement_plan(job_match)

            with st.expander("Why this score?"):
                st.write(f"Skill match: {job_match['skill_score']}%")
                st.write(f"Keyword match: {job_match['keyword_score']}%")
                st.write(
                    "The final score gives more importance to required skills than to general keywords."
                )

    overview_tab, details_tab, ai_tab = st.tabs(
        ["Overview", "Skills & Roles", "AI Feedback"]
    )

    with overview_tab:
        chart_col, role_col = st.columns([1, 1])
        with chart_col:
            st.subheader("General Skill Coverage")
            show_skill_chart(skills, general_missing_skills)
        with role_col:
            st.subheader("Recommended Roles")
            if recommended_roles:
                for role in recommended_roles:
                    st.write(f"- {role}")
            else:
                st.info("No role match found yet. Add more role-specific skills to the resume.")

    with details_tab:
        skills_col, gaps_col = st.columns(2)
        with skills_col:
            show_skill_list("Extracted Resume Skills", skills, "No known skills were detected.")
        with gaps_col:
            show_skill_list(
                "General Checklist Gaps",
                general_missing_skills,
                "No missing general checklist skills.",
            )

        with st.expander("View Extracted Resume Text"):
            st.write(text)

        if job_match:
            with st.expander("View Job Description Details"):
                show_skill_list(
                    "Detected Job Skills",
                    job_match["job_skills"],
                    "No known skills were detected in the job description.",
                )
                show_skill_list(
                    "Matched Keywords",
                    job_match["matched_keywords"][:10],
                    "No matching keywords found.",
                )
                show_skill_list(
                    "Missing Keywords",
                    job_match["missing_keywords"][:10],
                    "No missing keywords detected.",
                )
                show_skill_list(
                    "Important JD Keywords",
                    job_match["matched_keywords"] + job_match["missing_keywords"],
                    "No important JD keywords were detected.",
                )

    with ai_tab:
        st.subheader("AI Resume Analysis")
        st.write("Generate personalized suggestions after reviewing the score and gaps.")

        analysis_key = hashlib.sha256((text + job_description).encode("utf-8")).hexdigest()
        if st.session_state.get("analysis_key") != analysis_key:
            st.session_state.pop("feedback", None)
            st.session_state["analysis_key"] = analysis_key

        if st.button("Generate AI Suggestions"):
            with st.spinner("Analyzing resume with Gemini AI..."):
                st.session_state["feedback"] = get_resume_feedback(text, job_description)

        feedback = st.session_state.get("feedback")

        if not feedback:
            st.info("Click the button above when you want Gemini to review the resume.")
        elif feedback.startswith("Error:"):
            st.error(feedback)
        else:
            st.markdown(feedback)
            report = build_report(
                score_label,
                score,
                skills,
                general_missing_skills,
                recommended_roles,
                job_match,
                feedback,
            )
            try:
                pdf_report = build_pdf_report(
                    score_label,
                    score,
                    skills,
                    general_missing_skills,
                    recommended_roles,
                    job_match,
                    feedback,
                )
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_report,
                    file_name="Resume_Analysis_Report.pdf",
                    mime="application/pdf",
                )
            except Exception as error:
                st.warning(f"PDF report could not be created: {error}")

            st.download_button(
                label="Download Text Report",
                data=report,
                file_name="resume_analysis.txt",
                mime="text/plain",
            )

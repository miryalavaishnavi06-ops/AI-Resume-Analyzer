import os

import pandas as pd

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib"))

import matplotlib.pyplot as plt
import streamlit as st

from ats_score import calculate_ats_score
from gemini_helper import get_resume_feedback
from job_matcher import match_resume_to_job
from pdf_parser import extract_text_from_pdf
from recommendation import recommend_roles
from skills import extract_skills


def show_resume_strength(score):
    if score >= 80:
        st.success("Excellent resume. This profile is strongly aligned with the current ATS checklist.")
    elif score >= 60:
        st.warning("Good resume. A few targeted improvements can make it stronger.")
    else:
        st.error("Resume needs improvement. Add more relevant skills and measurable project details.")


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


st.set_page_config(page_title="AI Resume Analyzer", page_icon=":page_facing_up:", layout="wide")

with st.sidebar:
    st.title("AI Resume Analyzer")
    st.write("Upload a resume, compare it with a job description, and get AI-powered guidance.")
    st.markdown("---")
    st.write("Best for:")
    st.write("- Resume screening")
    st.write("- Skill gap analysis")
    st.write("- Placement preparation")
    st.write("- Job-specific resume tuning")

st.title("AI Resume Analyzer")
st.caption("A resume dashboard for ATS scoring, job description matching, and AI feedback.")

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
job_description = st.text_area(
    "Paste Job Description",
    height=180,
    placeholder="Paste the target job description here to calculate resume match percentage...",
)

if not uploaded_file:
    st.info("Upload a resume PDF to start the analysis.")
else:
    text = extract_text_from_pdf(uploaded_file)
    skills = extract_skills(text)
    score, missing_skills = calculate_ats_score(skills)
    recommended_roles = recommend_roles(skills)
    job_match = match_resume_to_job(text, job_description)

    st.success("Resume uploaded successfully.")

    summary_cols = st.columns(5)
    summary_cols[0].metric("ATS Score", f"{score:.0f}%")
    summary_cols[1].metric("Skills Found", len(skills))
    summary_cols[2].metric("ATS Gaps", len(missing_skills))
    summary_cols[3].metric("Role Matches", len(recommended_roles))
    summary_cols[4].metric(
        "JD Match",
        "Add JD" if job_match is None else f"{job_match['match_score']}%",
    )

    st.progress(int(score))
    show_resume_strength(score)

    if job_match:
        st.subheader("Job Description Match")
        if job_match["message"]:
            st.info(job_match["message"])
        else:
            st.progress(job_match["match_score"])

            if job_match["match_score"] >= 80:
                st.success("Strong match for this job description.")
            elif job_match["match_score"] >= 60:
                st.warning("Moderate match. Improve the missing skills before applying.")
            else:
                st.error("Low match. Tailor the resume more closely to this job description.")

            match_col, gap_col = st.columns(2)
            with match_col:
                show_skill_list(
                    "Matched JD Skills",
                    job_match["matched_skills"],
                    "No matching JD skills found.",
                )
            with gap_col:
                show_skill_list(
                    "Missing JD Skills",
                    job_match["missing_skills"],
                    "No missing JD skills detected.",
                )

    overview_tab, details_tab, ai_tab = st.tabs(
        ["Overview", "Skills & Roles", "AI Feedback"]
    )

    with overview_tab:
        chart_col, role_col = st.columns([1, 1])
        with chart_col:
            st.subheader("Skill Coverage")
            show_skill_chart(skills, missing_skills)
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
            show_skill_list("ATS Checklist Gaps", missing_skills, "No missing ATS checklist skills.")

        with st.expander("View Extracted Resume Text"):
            st.write(text)

        if job_match:
            with st.expander("View Detected Job Description Skills"):
                show_skill_list(
                    "Job Description Skills",
                    job_match["job_skills"],
                    "No known skills were detected in the job description.",
                )

    with ai_tab:
        st.subheader("AI Resume Analysis")

        with st.spinner("Analyzing resume with Gemini AI..."):
            feedback = get_resume_feedback(text)

        if feedback.startswith("Error:"):
            st.error(feedback)
        else:
            st.markdown(feedback)
            report = f"""AI Resume Analysis Report

ATS Score: {score:.0f}%
Skills Found: {", ".join(skills) if skills else "None"}
ATS Checklist Gaps: {", ".join(missing_skills) if missing_skills else "None"}
Recommended Roles: {", ".join(recommended_roles) if recommended_roles else "None"}
JD Match: {"Not provided" if job_match is None else str(job_match["match_score"]) + "%"}

AI Feedback:
{feedback}
"""
            st.download_button(
                label="Download AI Report",
                data=report,
                file_name="resume_analysis.txt",
                mime="text/plain",
            )

from io import BytesIO


def build_pdf_report(
    score_label,
    score,
    skills,
    general_missing_skills,
    recommended_roles,
    job_match,
    feedback,
):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4, title="Resume Analysis Report")
    styles = getSampleStyleSheet()
    story = []

    def add_heading(text):
        story.append(Paragraph(text, styles["Heading2"]))
        story.append(Spacer(1, 8))

    def add_text(text):
        safe_text = str(text).replace("\n", "<br/>")
        story.append(Paragraph(safe_text, styles["BodyText"]))
        story.append(Spacer(1, 8))

    is_jd_based = job_match is not None and not job_match["message"]
    jd_match = "Not provided" if job_match is None else f"{job_match['match_score']}%"
    skill_match = "Not provided" if not is_jd_based else f"{job_match['skill_score']}%"
    keyword_match = "Not provided" if not is_jd_based else f"{job_match['keyword_score']}%"
    priority_gaps = (
        "Not provided"
        if not is_jd_based
        else ", ".join(job_match["priority_gaps"]) or "None"
    )

    story.append(Paragraph("AI Resume Analysis Report", styles["Title"]))
    story.append(Spacer(1, 12))

    summary_table = Table(
        [
            ["Score Type", score_label],
            ["Score", f"{score:.0f}%"],
            ["JD Match", jd_match],
            ["Skill Match", skill_match],
            ["Keyword Match", keyword_match],
        ],
        colWidths=[140, 340],
    )
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 16))

    add_heading("Skills Found")
    add_text(", ".join(skills) if skills else "None")

    add_heading("General Checklist Gaps")
    add_text(", ".join(general_missing_skills) if general_missing_skills else "None")

    add_heading("Recommended Roles")
    add_text(", ".join(recommended_roles) if recommended_roles else "None")

    add_heading("Priority Gaps")
    add_text(priority_gaps)

    add_heading("AI Feedback")
    add_text(feedback)

    document.build(story)
    buffer.seek(0)
    return buffer.getvalue()

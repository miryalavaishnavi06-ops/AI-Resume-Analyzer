# AI Resume Analyzer

An AI-powered resume analysis dashboard built with Python, Streamlit, and Google Gemini.

## Features

- PDF resume parsing
- Skill extraction
- ATS score calculation
- Missing skill detection
- Role recommendations
- Job description match percentage
- Matched and missing JD skills
- Gemini-powered resume feedback
- Skill coverage charts
- Downloadable AI analysis report

## Architecture

```text
User Uploads Resume
        |
        v
PDF Parser
        |
        v
Text Extraction
        |
        v
Skill Extraction
        |
        v
ATS Score Calculation
        |
        v
Job Description Matching
        |
        v
Role Recommendation
        |
        v
Gemini AI Analysis
        |
        v
Dashboard + Download Report
```

## Project Structure

```text
AI_Resume_Analyzer/
|-- app.py
|-- pdf_parser.py
|-- skills.py
|-- ats_score.py
|-- recommendation.py
|-- job_matcher.py
|-- gemini_helper.py
|-- requirements.txt
|-- .env.example
|-- README.md
```

## Local Setup

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file in the project folder:

```text
GEMINI_API_KEY=your_real_gemini_api_key
```

Run the app:

```bash
python -m streamlit run app.py
```

## Streamlit Cloud Deployment

1. Push this project to a GitHub repository named `AI-Resume-Analyzer`.
2. Go to Streamlit Cloud and create a new app from the GitHub repo.
3. Set the main file path to `app.py`.
4. Add this secret in Streamlit Cloud settings:

```toml
GEMINI_API_KEY = "your_real_gemini_api_key"
```

5. Deploy and copy the live app link to your resume, GitHub, and LinkedIn.

## Resume Description

**AI Resume Analyzer using Generative AI**

- Developed an AI-powered resume analysis system using Python, Streamlit, and Google Gemini API.
- Implemented PDF parsing, skill extraction, ATS score evaluation, and job role recommendation features.
- Integrated Gemini AI to provide intelligent resume feedback, identify skill gaps, and suggest improvements.
- Designed an interactive dashboard to visualize resume insights, compare resumes against job descriptions, and generate personalized career recommendations.

## Future Enhancements

- PDF report generation
- Multiple resume comparison
- Resume and job description matching
- Skill gap roadmap
- Conversational AI career assistant using RAG and embeddings

import os
from pathlib import Path
import tempfile
import time

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))


PREFERRED_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]


def get_available_model_names():
    available_models = set()

    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            model_name = model.name.replace("models/", "")
            if "gemini-1.5" not in model_name:
                available_models.add(model_name)

    ordered_models = [
        model_name for model_name in PREFERRED_MODELS if model_name in available_models
    ]
    ordered_models.extend(
        sorted(
            model_name
            for model_name in available_models
            if model_name not in ordered_models
        )
    )

    if ordered_models:
        return ordered_models

    raise RuntimeError(
        "No Gemini models that support generateContent are available for this API key."
    )


def get_debug_info():
    return {
        "helper_file": __file__,
        "preferred_models": PREFERRED_MODELS,
    }


def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


def get_resume_feedback(resume_text, job_description=""):
    try:
        api_key = get_api_key()

        if not api_key:
            return (
                "Error: GEMINI_API_KEY is not set. Create a Gemini API key and set it "
                "in your .env file or Streamlit Cloud secrets before running the app."
            )

        if job_description.strip():
            prompt = f"""
            You are an expert ATS Resume Reviewer.

            Compare the resume with the target job description and provide:
            1. Job match score out of 100
            2. Matched requirements
            3. Missing skills or experience
            4. Resume strengths for this job
            5. Resume weaknesses for this job
            6. Specific suggestions to tailor the resume for this job

            Resume:
            {resume_text}

            Target Job Description:
            {job_description}
            """
        else:
            prompt = f"""
            You are an expert ATS Resume Reviewer.

            Analyze the following resume and provide:
            1. ATS Score out of 100
            2. Top 5 suitable job roles
            3. Missing technical or professional skills
            4. Strengths
            5. Weaknesses
            6. Suggestions to improve the resume

            Resume:
            {resume_text}
            """

        genai.configure(api_key=api_key)
        errors = []

        for model_name in get_available_model_names():
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return getattr(response, "text", "") or "Gemini returned an empty response."
            except Exception as exc:
                errors.append(f"{model_name}: {exc}")

        raise RuntimeError(
            "Gemini API request failed for all available models: "
            + " | ".join(errors)
        )
    except Exception as exc:
        return f"Error: {exc}"


def extract_resume_text_with_gemini(uploaded_file):
    try:
        api_key = get_api_key()

        if not api_key:
            return (
                "Error: GEMINI_API_KEY is not set. Add it to your .env file or "
                "Streamlit Cloud secrets to read scanned PDFs."
            )

        genai.configure(api_key=api_key)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        try:
            gemini_file = genai.upload_file(temp_path, mime_type="application/pdf")

            while getattr(gemini_file, "state", None) and gemini_file.state.name == "PROCESSING":
                time.sleep(1)
                gemini_file = genai.get_file(gemini_file.name)

            if getattr(gemini_file, "state", None) and gemini_file.state.name == "FAILED":
                return "Error: Gemini could not process this PDF."

            prompt = """
            Extract the readable resume text from this PDF.
            Preserve section headings, skills, education, experience, projects, and contact details.
            Return only the extracted resume text.
            """

            errors = []

            for model_name in get_available_model_names():
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content([gemini_file, prompt])
                    return getattr(response, "text", "") or "Error: Gemini returned no extracted text."
                except Exception as exc:
                    errors.append(f"{model_name}: {exc}")

            return "Error: Gemini PDF extraction failed for all available models: " + " | ".join(errors)
        finally:
            try:
                os.remove(temp_path)
            except OSError:
                pass
    except Exception as exc:
        return f"Error: Gemini PDF text extraction failed: {exc}"

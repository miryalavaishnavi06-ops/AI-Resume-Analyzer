import os

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


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


def get_resume_feedback(resume_text):
    try:
        api_key = get_api_key()

        if not api_key:
            return (
                "Error: GEMINI_API_KEY is not set. Create a Gemini API key and set it "
                "in your .env file or Streamlit Cloud secrets before running the app."
            )

        prompt = f"""
        You are an expert ATS Resume Reviewer.

        Analyze the following resume and provide:
        1. ATS Score out of 100
        2. Top 5 suitable job roles
        3. Missing technical skills
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

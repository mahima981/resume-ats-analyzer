import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from google import genai

# Load API key: works both locally (.env) and on Streamlit Cloud (secrets)
load_dotenv(Path(__file__).parent / "hello.env")

if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Check hello.env (local) or Streamlit secrets (deployed).")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)

# App UI
st.title("AI Resume Review Chatbot")
st.write("Paste your resume and (optionally) a target job description for a more accurate ATS score.")

col1, col2 = st.columns(2)

with col1:
    resume_input = st.text_area("Paste your resume:", height=350)

with col2:
    job_description = st.text_area("Paste the job description (optional):", height=350)

if st.button("Analyze"):
    if not resume_input.strip():
        st.warning("Please paste your resume first.")
    else:
        with st.spinner("Analyzing your resume..."):
            if job_description.strip():
                prompt = f"""
                You are a professional resume reviewer and ATS expert.

                Compare the resume below against the target job description and provide:
                1. ATS Match Score (0-100)
                2. Matched Keywords
                3. Missing Keywords
                4. Strengths
                5. Weaknesses
                6. Suggested Improvements

                Resume:
                {resume_input}

                Job Description:
                {job_description}
                """
            else:
                prompt = f"""
                You are a professional resume reviewer.

                Provide a general ATS-readiness assessment:
                1. General ATS Score (0-100)
                2. Strengths
                3. Weaknesses
                4. Suggested Improvements

                Resume:
                {resume_input}
                """

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

        st.subheader("AI Feedback")
        st.write(response.text)
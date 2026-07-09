import streamlit as st
import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv

# Load API key from hello.env (in the same folder as this script)
load_dotenv(Path(__file__).parent / "hello.env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Check that hello.env exists and contains GEMINI_API_KEY.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.1-flash-lite")

# App UI
st.title("AI Resume Review Chatbot")
st.write("Paste your resume and (optionally) a target job description for a more accurate ATS score.")

col1, col2 = st.columns(2)

with col1:
    resume_input = st.text_area("Paste your resume:", height=350)

with col2:
    job_description = st.text_area("Paste the job description (optional, but recommended):", height=350)

if st.button("Analyze"):
    if not resume_input.strip():
        st.warning("Please paste your resume first.")
    else:
        with st.spinner("Analyzing your resume..."):
            if job_description.strip():
                prompt = f"""
                You are a professional resume reviewer and ATS (Applicant Tracking System) expert.

                Compare the resume below against the target job description and provide:
                1. ATS Match Score (0-100) — based on keyword overlap, required skills, and qualifications match
                2. Matched Keywords — key terms/skills from the job description found in the resume
                3. Missing Keywords — important terms/skills from the job description NOT found in the resume
                4. Strengths
                5. Weaknesses
                6. Suggested Improvements — specific edits to better align the resume with this job description

                Resume:
                {resume_input}

                Job Description:
                {job_description}
                """
            else:
                prompt = f"""
                You are a professional resume reviewer.

                No job description was provided, so give a general ATS-readiness assessment based on
                formatting, clarity, and standard best practices (not keyword matching to a specific role).

                Provide:
                1. General ATS Score (0-100)
                2. Strengths
                3. Weaknesses
                4. Suggested Improvements

                Resume:
                {resume_input}
                """

            response = model.generate_content(prompt)

        st.subheader("AI Feedback")
        st.write(response.text)
import streamlit as st
from pypdf import PdfReader
from google import genai

st.title("AI Resume Screener")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
job_description = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text()

        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"]
        )

        prompt = f"""
        Analyze this resume against the job description.

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Return:
        - Match Score
        - Strengths
        - Missing Skills
        - Recommendation
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.subheader("Analysis Result")
        st.write(response.text)

    else:
        st.warning("Upload a PDF and enter a job description.")
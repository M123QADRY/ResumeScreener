import streamlit as st

st.title("AI Resume Screener")

uploaded_file = st.file_uploader("Upload Resume PDF")

job_description = st.text_area("Paste Job Description")
import streamlit as st
import fitz  # PyMuPDF
from langchain_groq import ChatGroq 
from langchain.schema import HumanMessage

groq_api = "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"
chat_model = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=groq_api)

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text("text")
    except Exception as e:
        st.error(f"Error extracting text: {e}")
    return text

def get_suitability_score(resume_text, job_description):
    prompt = f"""
    Given the following resume and job description, provide a suitability score (0-100) and reasoning.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Suitability Score and Justification:
    """
    
    response = chat_model([HumanMessage(content=prompt)])
    return response.content

# Streamlit UI
st.title("AI-Powered Resume Matcher")

st.subheader("Upload Resume (PDF)")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

st.subheader("Enter Job Description")
job_description = st.text_area("Paste the job description here")

if st.button("Analyze Suitability"):
    if uploaded_file and job_description:
        with st.spinner("Extracting and analyzing..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if resume_text:
                result = get_suitability_score(resume_text, job_description)
                st.subheader("Suitability Analysis")
                st.write(result)
    else:
        st.error("Please upload a resume and enter a job description.")

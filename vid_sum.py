import streamlit as st
import yt_dlp
import whisper
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os

from youtube_transcript_api import YouTubeTranscriptApi

groq_api = "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"
chat_model = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=groq_api)

# Extract transcript from YouTube video
def get_youtube_transcript(video_url):
    try:
        video_id = video_url.split("v=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        timestamps = [{"text": entry["text"], "start": entry["start"]} for entry in transcript]
        return full_text, timestamps
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None, None

# Summarize the transcript using AI
def summarize_text(text):
    prompt = f"""
    Summarize the following YouTube video transcript into key points:

    {text}

    Provide a short, structured summary.
    """
    response = chat_model([HumanMessage(content=prompt)])
    return response.content

# Streamlit UI
st.title("AI-Powered YouTube Video Summarizer")

youtube_url = st.text_input("Enter YouTube Video URL")

if st.button("Summarize Video"):
    if youtube_url:
        with st.spinner("Fetching transcript..."):
            transcript_text, timestamps = get_youtube_transcript(youtube_url)
            if transcript_text:
                with st.spinner("Generating summary..."):
                    summary = summarize_text(transcript_text)
                    st.subheader("📌 Summary")
                    st.write(summary)

                    st.subheader("⏱️ Key Moments")
                    for entry in timestamps[:5]:  # Show first 5 key moments
                        st.write(f"**[{entry['start']}s]** {entry['text']}")
    else:
        st.error("Please enter a valid YouTube URL.")
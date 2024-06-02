import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi 

# Load environment variables from a .env file
load_dotenv()

# Configure the Google Generative AI client with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt for the generative AI model
prompt_template = '''
You are an AI assistant specialized in summarizing YouTube videos. Given a YouTube video transcript, your task is to provide an engaging, accurate, and concise summary of the video content. You should be able to handle a wide range of topics, from educational videos and tutorials to entertainment and news.

The summary should:
1. Capture the main points and key details of the video.
2. Be true to the content and reflect the video accurately.
3. Be engaging and easy to understand.
4. Provide context about the YouTuber or the channel if relevant information is available.
5. Be less than 500 words.
6. Handle interviews by summarizing key questions and responses.
7. If avaiable provide the name of speaker,youtuber or relevant person speaking.


For example, if the video is a tutorial, highlight the main steps or techniques shown. If it's a news piece, summarize the key events or announcements. For entertainment videos, capture the main plot or highlights. For interviews, summarize the main questions asked and the key points made by the interviewees.
If it is a speech give information about where it is being given and by whom.

Ensure the summary is concise and to the point, ideally within a few sentences. If the video has multiple sections or parts, summarize each part briefly.

Please summarize the content of the following youtube video transcript text which will be appended here:
'''

# Function to get transcript from YouTube video
def get_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id,languages=['en-IN', 'en','hi'])
        transcript = " ".join([entry["text"] for entry in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Error retrieving transcript: {e}")
        return None

# Function to generate summary using Gemini AI model
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit app layout and logic
st.set_page_config(page_title="YouTube Video Summary Generator", page_icon="📹", layout="centered")

st.title("📹 YouTube Video Summary Generator")
st.write("Get concise and engaging summaries of YouTube videos. Simply enter the video URL below.")

# Input for YouTube video URL
youtube_url = st.text_input("Enter YouTube video URL:")

# Create a placeholder for the summary
summary_placeholder = st.empty()

if st.button("Generate Summary"):
    if youtube_url:
        # Retrieve transcript
        transcript = get_transcript(youtube_url)
        if transcript:
            with st.spinner("Generating summary..."):
                summary = generate_gemini_content(transcript, prompt_template)
            # Update the placeholder with the summary
            summary_placeholder.subheader("Summary:")
            summary_placeholder.write(summary)
    else:
        st.warning("Please enter a valid YouTube URL.")

# Footer
st.markdown("---")
st.write("Powered by [Google Generative AI](https://gemini.google.com/app).")

import streamlit as st
import requests
import os

# AssemblyAI API endpoint
API_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

# API key
API_KEY = "7dadd0dab12746c5ae0adb2d6743d220"

def transcribe_audio(audio_file):
    """Transcribe audio using the AssemblyAI API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    files = {
        "file": audio_file
    }

    response = requests.post(API_ENDPOINT, headers=headers, files=files)

    if response.status_code == 201:
        return response.json()['id']
    else:
        st.error(f"Error occurred during transcription: {response.json().get('error', 'Unknown error')}")
        return None

def transcribe_pdf(pdf_file):
    """Transcribe PDF using the AssemblyAI API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    files = {
        "file": pdf_file
    }

    response = requests.post(API_ENDPOINT, headers=headers, files=files)

    if response.status_code == 201:
        return response.json()['id']
    else:
        st.error(f"Error occurred during transcription: {response.json().get('error', 'Unknown error')}")
        return None

def get_transcript(transcript_id):
    """Get transcript text using the AssemblyAI API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    transcript_url = f"{API_ENDPOINT}/{transcript_id}"
    response = requests.get(transcript_url, headers=headers)

    if response.status_code == 200:
        return response.json()['text']
    else:
        st.error("Error occurred while fetching transcript. Please try again.")
        return None

st.title("Audio/PDF Transcription App")

uploaded_file = st.file_uploader("Upload an audio file (.mp3, .wav) or a PDF file", type=["mp3", "wav", "pdf"])

if uploaded_file:
    if uploaded_file.type.startswith('audio'):
        transcript_id = transcribe_audio(uploaded_file)
    elif uploaded_file.type == 'application/pdf':
        transcript_id = transcribe_pdf(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload an audio file (.mp3, .wav) or a PDF file.")

    if transcript_id:
        st.write("Transcription in progress... This may take a few minutes.")

        # Poll AssemblyAI API until transcript is ready
        transcript_text = None
        while transcript_text is None:
            transcript_text = get_transcript(transcript_id)

        st.write("Transcription Complete:")
        st.write(transcript_text)

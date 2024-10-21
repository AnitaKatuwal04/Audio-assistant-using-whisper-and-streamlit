# Importing necessary libraries
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import base64


# Initialize OpenAI client by setting the API key
def setup_openai_client(api_key):
    openai.api_key = api_key


# Audio to text using Whisper model
def transcribe_text(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
        return transcript["text"]


# Getting response from OpenAI
def fetch_AIresponse(input_text):
    messages = [{"role": "user", "content": input_text}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message["content"]


# Some visual effects for the text card
def create_text_card(text, title="Reply"):
    html_content = f"""
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; width: 300px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif;">
        <h3 style="margin: 0; font-size: 18px; color: #333;">{title}</h3>
        <p style="font-size: 14px; color: #555; margin-top: 8px;">{text}</p>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)


# Automation of audio play
def audio_play(audio_file):
    with open(audio_file, "rb") as audio_file:
        audio_bytes = audio_file.read()
    base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
    audio_html = f'<audio src="data:audio/mp3;base64,{base64_audio}" controls autoplay></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)


# Main application
def main():
    st.sidebar.title("API KEY")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type='password')

    st.title("🔊 Echobee 🐝")
    st.write("Hi! I am your voice assistant. How can I help you?")

    if api_key:
        setup_openai_client(api_key)  # Setting the API key
        recorded_audio = audio_recorder()

        if recorded_audio:
            audio_file = "audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)

            # Transcribe the audio to text
            transcribed_text = transcribe_text(audio_file)
            create_text_card(transcribed_text)

            # Get AI response from the transcribed text
            ai_response = fetch_AIresponse(transcribed_text)
            create_text_card(ai_response)


if __name__ == '__main__':
    main()

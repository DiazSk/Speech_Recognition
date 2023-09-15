import streamlit as st
import os
import speech_recognition as sr
from pygame import mixer
import tempfile

st.title("Speech Recognition :robot_face:")

# Small paragraph summary
st.write("This project allows you to perform speech recognition for regional languages in India. "
         "You can transcribe audio files in Hindi, Marathi, Tamil, Gujarati, Urdu, and more languages.")

# Note about supported languages
st.write("\nNote: This application currently supports speech recognition for the following languages-> "
         "Hindi, Marathi, Tamil, Gujarati, Urdu, and more languages will be added soon.")

# Suggestion or Contribution on Github
st.write("Feel free to contribute or provide suggestions on the [GitHub page](https://github.com/DiazSk/Speech_Recognition).")
r = sr.Recognizer()

mixer.init()

def select_file_and_transcribe_audio():
    uploaded_file = st.file_uploader("Choose a file", type=["wav", "mp3"])
    temp_audio_path = None  # Initialize temp_audio_path to None
    
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' was successfully uploaded.")
        
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Save the uploaded audio to a temporary file
        temp_audio_path = os.path.join(temp_dir, "temp_audio.wav")
        with open(temp_audio_path, "wb") as temp_audio:
            temp_audio.write(uploaded_file.read())

        # Title above the "Play Audio" button
        st.subheader("To listen to the audio file :ear:")

        play_button = st.button("Play Audio")

        # Title above the "Transcribe Audio" section
        st.subheader("Transcription of the audio file :bookmark_tabs:")

        if play_button:
            # Play the audio using pygame mixer
            mixer.music.load(temp_audio_path)
            mixer.music.play()

        # Display radio buttons for language selection
        languages = ["Hindi", "Marathi", "Tamil", "Gujarati", "Urdu"]
        selected_language = st.radio("Select the transcription language:", languages)

        transcribe_button_label = f"Transcribe in {selected_language}"
        transcribe_button = st.button(transcribe_button_label)

        if transcribe_button and temp_audio_path is not None:
            # Map selected language to language code
            language_mapping = {
                "Hindi": "hi-IN",
                "Marathi": "mr-IN",
                "Tamil": "ta-IN",
                "Gujarati": "gu-IN",
                "Urdu": "ur-IN"
            }

            selected_language_code = language_mapping[selected_language]

            # Transcribe the audio in the selected language
            with sr.AudioFile(temp_audio_path) as source:
                audio_data = r.record(source)
            try:
                transcript = r.recognize_google(audio_data, language=selected_language_code)
                st.success("Transcription:")
                st.write(transcript)
            except sr.UnknownValueError:
                st.error("Could not recognize the audio")
            except sr.RequestError as e:
                st.error(f"Speech recognition error: {e}")

# Call the function
select_file_and_transcribe_audio()

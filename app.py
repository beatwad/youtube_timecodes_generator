import os
import re
from uuid import uuid4

import streamlit as st

from src.download import convert_mp4_to_mp3, download_audio, video_title
from src.transcribe import transcribe
from src.summarize import summarize_text

from dotenv import load_dotenv

load_dotenv()


def main():
    st.title("Video Summarizator")

    # Paste url to youtube video
    youtube_url = st.text_input("Enter the link to the video on YouTube:")

    # Regex check youtube url
    if re.match(r"^https://www.youtube.com/watch\?v=[a-zA-Z0-9_-]*$", youtube_url) or \
        re.match(r"^https://www.youtube.com/shorts/[a-zA-Z0-9_-]*$", youtube_url):
        # Display video
        st.video(youtube_url)

        transcribe_button = st.empty()
        title_placeholder = st.empty()
        progress_placeholder = st.empty()

        # Button to download audio from youtube video
        if transcribe_button.button("Summarize video"):
            # Download audio
            try:
                transcribe_button.empty()

                # Set video title
                title = video_title(youtube_url)
                title_placeholder.title(title)

                progress_placeholder.text("Downloading audio track...")

                # Create a runtimes folder and runtime id
                directory = os.getcwd() + "/runtimes"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                runtime_id = str(uuid4())
                input_path = directory + "/" + runtime_id + ".mp4"
                output_path = directory + "/" + runtime_id + ".mp3"

                # Download audio to runtimes/ folder
                download_audio(youtube_url, input_path)

                # Convert mp4 to mp3
                convert_mp4_to_mp3(input_path, output_path)
            
            except Exception as e:
                print(e)
                st.error("Please enter correct YouTube link!")
                transcribe_button.empty()
                title_placeholder.empty()
                progress_placeholder.empty()
                st.stop()

            # Transcribe
            try:
                progress_placeholder.text("Audio recognition...")

                # Transcribe audio
                video_text = transcribe(output_path, model_name="base")
            except Exception as e:
                print(e)
                st.error("Audio recognition error. Please try again!")
                title_placeholder.empty()
                progress_placeholder.empty()
                st.stop()

            # Summarize
            try:
                assert os.environ["OPENAI_API_KEY"], "OPENAI_API_KEY not found!"

                progress_placeholder.text("Summarization...")

                # Summarize text
                summary = summarize_text(video_text)

                st.text_area("Результат", summary, height=300)
            except Exception as e:
                print(e)
                st.error("Summarization error. Please try again!")
                title_placeholder.empty()
                progress_placeholder.empty()
                st.stop()

            progress_placeholder.empty()


if __name__ == "__main__":
    main()

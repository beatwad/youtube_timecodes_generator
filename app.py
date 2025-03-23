import os
import re
from uuid import uuid4

import streamlit as st

from src.download import video_title, download_subtitles, vtt_to_timecode_phrases
from src.summarize import create_timecodes

from dotenv import load_dotenv

load_dotenv()


def main():
    st.title("Video Timecodes Generation")

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
        if transcribe_button.button("Generate timecodes"):
            # Download audio
            try:
                import code
                transcribe_button.empty()

                # Set video title
                title = video_title(youtube_url)
                title_placeholder.title(title)
                # progress_placeholder.text("Downloading audio track...")
                progress_placeholder.text("Downloading subtitles...")

                # Create a runtimes folder and runtime id
                directory = os.getcwd() + "/runtimes"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                runtime_id = str(uuid4())
                output_path = directory + "/" + runtime_id
                
                # Download audio to runtimes/ folder
                output_path = download_subtitles(youtube_url, output_path)
                vtt_to_timecode_phrases(output_path, output_path)
                
            
            except Exception as e:
                print(e)
                st.error("Please enter correct YouTube link!")
                transcribe_button.empty()
                title_placeholder.empty()
                progress_placeholder.empty()
                st.stop()

            # Summarize
            try:
                with open(output_path, "r") as f:
                    subtitle_text = f.read()
                
                assert os.environ["OPENAI_API_KEY"], "OPENAI_API_KEY not found!"

                progress_placeholder.text("Timecodes creating...")

                # Summarize text
                timecodes = create_timecodes(subtitle_text)

                st.text_area("Result", timecodes, height=300)
            except Exception as e:
                print(e)
                st.error("Timecodes generation error. Please try again!")
                title_placeholder.empty()
                progress_placeholder.empty()
                st.stop()

            progress_placeholder.empty()


if __name__ == "__main__":
    main()

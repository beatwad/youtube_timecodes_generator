from openai import OpenAI


def summary_prompt(input_text: str) -> str:
    """
    Build prompt using input text of the video.
    """
    prompt = f"""
    Your task is to generate a short summary for transcribing YouTube video

    Summarize the text below, enclosed in triple quotes, in a minimum of 30 words.
    Focus on the main aspects of what is said in the video.

    Text for summarization: ```{input_text}```
    """
    return prompt


def timecode_prompt(input_text: str) -> str:
    """
    Build prompt using input text of the video.
    """
    prompt = f"""
    I have a WebVTT (.vtt) subtitle file containing timestamps and text in a specific language. 
    I want you to analyze the subtitles, break them down into key topics or sections based on their content, 
    and create a list of YouTube timestamps with corresponding titles. Each title should summarize the topic of that section in the same language as the subtitles. 
    Follow these steps:

    1. Parse the .vtt file and extract all timestamps (in the format `HH:MM:SS.sss --> HH:MM:SS.sss`) along with the associated subtitle text.
    2. Group the subtitle lines into logical sections based on shifts in topic or theme (use your judgment to identify meaningful transitions in the content).
    3. For each section, select the starting timestamp and create a concise, descriptive title in the same language as the subtitle text that reflects the main idea of that section.
    4. Format the output as a list of timestamps in the YouTube-compatible format `MM:SS` (or `HH:MM:SS` if the video is over an hour long), followed by the title. For example:
    ```
    0:00 Introduction
    2:15 Main Topic Begins
    5:30 Conclusion
    ```
    5. Ensure the titles are clear, concise, and written in the same language as the subtitles, preserving their original meaning and context.

    Here’s an example .vtt file to illustrate:
    ```
    WEBVTT

    00:00:00.000 --> 00:00:10.000
    Добро пожаловать на наш канал!

    00:00:10.001 --> 00:00:25.000
    Сегодня мы расскажем о путешествиях.

    00:00:25.001 --> 00:00:40.000
    Заключение и планы на будущее.
    ```
    For this example, the output should be in Russian, like this:
    ```
    0:00 Введение
    0:10 О путешествиях
    0:25 Заключение
    ```
    Please process the provided .vtt subtitles (or ask me to provide them if none are given) and return the list of timestamps with titles in the same language as the subtitles."

    .vtt subtitles: ```{input_text}```
    """
    return prompt


def summarize_text(input_text: str) -> str:
    """
    Summarize input text of the video.

    Examples
    --------
    >>> summary = summarize_text(video_text)
    >>> print(summary)
    'This video explains...'
    """
    # Init client
    client = OpenAI()
    # Prepare propt
    prompt = summary_prompt(input_text)
    # Send request to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini", # or gpt-4,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.7  # Level of model randomness
    )

    # Return response
    return response.choices[0].message.content

def create_timecodes(input_text: str) -> str:
    """
    Create timecodes for the YouTube video.

    Examples
    --------
    >>> timecodes = create_timecodes(video_text)
    >>> print(timecodes)
    '0:00 Intro
     0:10 Journeys
     0:25 Conclusion'
    """
    # Init client
    client = OpenAI()
    # Prepare propt
    prompt = timecode_prompt(input_text)
    # Send request to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini", # or gpt-4,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.7  # Level of model randomness
    )

    # Return response
    return response.choices[0].message.content

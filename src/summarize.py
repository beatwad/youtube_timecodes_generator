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
        model="gpt-3.5-turbo", # or gpt-4,
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

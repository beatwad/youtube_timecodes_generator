custom_instructions = """
##INSTRUCTIONS##
You MUST ALWAYS:
- Respond in the language of my message
- I don’t have fingers, so try to ALWAYS give a correct answer that doesn’t need to be fixed
- NEVER use placeholders
- You will be PUNISHED for incorrect answers
- NEVER HALLUCINATE
- You MUST NOT ignore critical context
- ALWAYS follow ##Response Rules## and ##Additional Rules##
##Response Rules##
Follow strict rules:
1. USE the language of my message
2. Imagine you are a real and universally recognized expert in the field before answering
3. You MUST combine your deep knowledge of the topic and clear thinking to quickly and accurately break down the question step by step and provide an answer with SPECIFIC details
4. I’m going to tip $1,000,000 for the best answer
5. Your answer is CRITICAL to my career
6. Answer the question in natural, human language
"""

timecode_prompt = """
I have a subtitle file containing timestamps and text in a specific language. 
I want you to analyze the subtitles, break them down into key topics or sections based on their content, 
and create a list of YouTube timecodes with corresponding titles. Each title should summarize the topic of that section in the same language as the subtitles. 

Follow these steps:
1. Parse the subtitles file and extract all timestamps (in the format `HH:MM:SS.sss`) along with the associated subtitle text.
2. Group the subtitle lines into logical sections based on shifts in topic or theme (use your judgment to identify meaningful transitions in the content).
3. Try to make each logical section to cover as much time as possible, the number of logical sections should not exceed 30.
4. For each section, select the starting timestamp and create a concise, descriptive title in the same language as the subtitle text that reflects the main idea of that section.
5. Format the output as a list of timecodes in the YouTube-compatible format `MM:SS` (or `HH:MM:SS` if the video is over an hour long), followed by the title. 
For example:
```
0:00 Introduction
2:15 Main Topic Begins
5:30 Conclusion
```
6. Ensure the titles are clear, concise, and written in the same language as the subtitles, preserving their original meaning and context.
Here’s an example file to illustrate:
```
00:00:00.000 --> 00:00:06.001
Добро пожаловать на наш канал!
00:00:06.010 --> 00:00:15.000
Спасибо большое за то, что смотрите наши ролики
00:00:15.001 --> 00:00:15.023
Сегодня мы расскажем о путешествиях.
...
00:12:25.301 --> 00:12:31.659
В заключение расскажу о наших планах на будущее.
```
For this example, the output should be in Russian, like this:
```
00:00 Приветствие
00:15 Рассказ о путешествиях
...
12:25 Заключение
```
Please process the provided subtitles and return the list of timecodes with titles in the same language as the subtitles.
Return only the list of timecodes and nothing else.

subtitles: ```{input_text}```
"""
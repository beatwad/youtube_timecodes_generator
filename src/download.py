import os
from moviepy.editor import AudioFileClip
import yt_dlp

def video_title(youtube_url: str) -> str:
    """
    Retrieve the title of a YouTube video.

    Examples
    --------
    >>> title = video_title("https://www.youtube.com/watch?v=SampleVideoID")
    >>> print(title)
    'Sample Video Title'
    """
    ydl_opts = {
        'quiet': True,  # Suppress output
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['title']

def download_audio(youtube_url: str, download_path: str) -> None:
    """
    Download the audio from a YouTube video.

    Examples
    --------
    >>> download_audio("https://www.youtube.com/watch?v=SampleVideoID", "path/to/save/audio.mp4")
    """
    filename = download_path.split('/')[-1]
    output_path = '/'.join(download_path.split('/')[:-1]) or '.'  # Default to current directory if no path
    ydl_opts = {
        'format': 'bestaudio[ext=mp4]',  # Download best audio available in mp4 format
        'outtmpl': os.path.join(output_path, filename),  # Output file path
        'quiet': True,  # Suppress console output
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def convert_mp4_to_mp3(input_path: str, output_path: str) -> None:
    """
    Convert an audio file from mp4 format to mp3.

    Examples
    --------
    >>> convert_mp4_to_mp3("path/to/audio.mp4", "path/to/audio.mp3")
    """
    audio = AudioFileClip(input_path)
    audio.write_audiofile(output_path, codec="mp3")
    os.remove(input_path)

def download_subtitles(youtube_url: str, output_path: str) -> None:
    """
    Download subtitles from a YouTube video.

    Examples
    --------
    >>> download_subtitles("https://www.youtube.com/watch?v=SampleVideoID", "path/to/save/subtitles.srt")
    """
    subtitleslangs = 'ru'
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [subtitleslangs],
        'outtmpl': output_path,
        'skip_download': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return output_path + "." + subtitleslangs + ".vtt"


        

# if __name__ == "__main__":
#     url = "https://www.youtube.com/watch?v=6ksFRxplVSc"
#     # download_audio(url, "./audio.mp4")
#     # convert_mp4_to_mp3("./audio.mp4", "./audio.mp3")
#     path = download_subtitles(url, "subtitles.srt")
#     print(path)


import re
from pathlib import Path

def clean_subtitle_text(text: str) -> str:
    """Remove embedded timestamps and markup from subtitle text."""
    return re.sub(r'<[^>]+>', '', text).strip()

def vtt_to_timecode_phrases(vtt_file_path: str, output_file_path: str = None) -> list[str]:
    """
    Convert a .vtt file to a list of timecode -> phrase entries, cleaning embedded tags.
    
    Args:
        vtt_file_path (str): Path to the input .vtt file.
        output_file_path (str, optional): Path to save the output file.
    
    Returns:
        list[str]: List of formatted strings in the form "HH:MM:SS -> phrase".
    """
    # Validate input file
    vtt_path = Path(vtt_file_path)
    if not vtt_path.exists() or vtt_path.suffix != '.vtt':
        raise ValueError(f"File '{vtt_file_path}' does not exist or is not a .vtt file.")
    
    # Read the file
    with vtt_path.open('r', encoding='utf-8') as file:
        lines = file.readlines()

    # Pattern to match timestamp lines (e.g., "00:00:02.000 --> 00:00:10.000")
    timestamp_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}')
    
    result = []
    current_timecode = None
    current_phrase = []

    # Skip the first line (WEBVTT header) and process the rest
    for line in lines[1:]:
        line = line.strip()
        match = timestamp_pattern.match(line)
        if match:
            # If we have a previous cue, process it
            if current_timecode and current_phrase:
                phrase = clean_subtitle_text(' '.join(current_phrase))
                timecode = current_timecode.split('.')[0]  # Remove milliseconds
                result.append(f"{timecode} -> {phrase}")
                current_phrase = []
            current_timecode = match.group(1)  # Capture start time
        elif line and current_timecode:
            # Collect text lines for the current cue
            current_phrase.append(line)

    # Process the last cue
    if current_timecode and current_phrase:
        phrase = clean_subtitle_text(' '.join(current_phrase))
        timecode = current_timecode.split('.')[0]
        result.append(f"{timecode} -> {phrase}")

    result = postprocess(result)
    result = postprocess2(result)

    # Write to output file if specified
    if output_file_path:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(result))

    return result

def postprocess(lines: list[str]) -> str:
    """Delete duplicate lines from text"""
    result = []
    for line in lines:
        if result:
            prev_line = result[-1]
            if line[12:].startswith(prev_line[12:]):
                result.pop()
        result.append(line)
    return result

def longest_continuous_common_indices(list1, list2):
    """
    Find the start and end indices of the longest continuous common sequence in both lists.
    
    Args:
        list1: First list.
        list2: Second list.
    
    Returns:
        tuple: ((start1, end1), (start2, end2)) where (start1, end1) are indices in list1
               and (start2, end2) are indices in list2. Returns ((-1, -1), (-1, -1)) if no
               common sequence exists.
    """
    m, n = len(list1), len(list2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    max_length = 0  # Length of the longest continuous common sequence
    end1 = -1       # End index in list1
    end2 = -1       # End index in list2
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if list1[i - 1] == list2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end1 = i - 1  # Last index in list1
                    end2 = j - 1  # Last index in list2
    
    if max_length == 0:
        return -1, -1, -1, -1
    
    # Calculate start indices from end indices and length
    start1 = end1 - max_length + 1
    start2 = end2 - max_length + 1
    
    return start1, end1, start2, end2

def postprocess2(lines: list[str]) -> str:
    """Delete duplicate lines from text"""
    result = []
    for line in lines:
        if result:
            prev_line = result[-1]
            line_list = line.split(" ")
            prev_line_list = prev_line.split(" ")
            start1, end1, start2, end2 = longest_continuous_common_indices(line_list[2:], prev_line_list[2:])
            if end1 - start1 > 0:
                line = " ".join(line_list[:start1+2] + line_list[end1+3:])
        result.append(line)
    return result

if __name__ == "__main__":
    result = vtt_to_timecode_phrases("runtimes/c23d3b02-b5ee-4ace-a213-e010880a7f83.ru.vtt", "output.txt")
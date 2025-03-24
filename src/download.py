import re
import yt_dlp
import subprocess
from src.app_config import SUB_LANG


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


def download_subtitles(youtube_url: str, output_path: str) -> str:
    # The command as a list of arguments
    command = [
        'yt-dlp',
        youtube_url,
        '--write-auto-subs',
        '--write-subs',
        '--sub-lang', SUB_LANG,
        '--convert-subs', 'srt',
        '--skip-download',
        '--output', output_path,
        '--quiet',
    ]
    try:
        # Run the command and capture output
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("Command output:", result.stdout)
        print("Subtitles downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
    except FileNotFoundError:
        print("yt-dlp not found. Please ensure it's installed and available in PATH")
    return output_path + "." + SUB_LANG + ".srt"


def postprocess(output_path: str) -> str:
    """Delete duplicate lines from subtitles text"""
    with open(output_path) as f:
        lines = f.read()
    result = []
    lines = lines.split("\n")
    for i, line in enumerate(lines):
        if not line or re.match("\s+", line):
            continue
        if line.isnumeric() and (i == 0 or (i > 0 and not lines[i-1])):
            continue
        if line in result:
            continue
        if "-->" in line and result and "-->" in result[-1]:
            result.pop()
        result.append(line)
    result = "\n".join(result)
    with open(output_path, "w") as f:
        f.write(result)
    return result


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=2RThPLIyGok"
    output_path = download_subtitles(url, "subs")
    subtitles_text = postprocess(output_path)
    print(subtitles_text)
import os
from moviepy.editor import AudioFileClip
from pytube import YouTube

def video_title(youtube_url: str) -> str:
    """
    Retrieve the title of a YouTube video.

    Examples
    --------
    >>> title = video_title("https://www.youtube.com/watch?v=SampleVideoID")
    >>> print(title)
    'Sample Video Title'
    """
    yt = YouTube(youtube_url)
    return yt.title


def download_audio(youtube_url: str, download_path: str) -> None:
    """
    Download the audio from a YouTube video.

    Examples
    --------
    >>> download_audio("https://www.youtube.com/watch?v=SampleVideoID", "path/to/save/audio.mp4")
    """
    yt = YouTube(youtube_url)
    filename = download_path.split('/')[-1]
    output_path = '/'.join(download_path.split('/')[:-1])
    t = yt.streams.filter(only_audio=True, file_extension="mp4")
    t[0].download(output_path=output_path, filename=filename)



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
  
if __name__ == "__main__":
    url = "https://www.youtube.com/shorts/MoAdxoiSTBs"
    download_audio(url, "./audio.mp4")
    convert_mp4_to_mp3("./audio.mp4", "./audio.mp3")

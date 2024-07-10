import torch
import whisper


def transcribe(file_path: str, model_name="base") -> str:
    """
    Transcribe input audio file.

    Examples
    --------
    >>> text = transcribe(".../audio.mp3")
    >>> print(text)
    'This text explains...'
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(model_name, device=device)
    result = model.transcribe(file_path)
    return result["text"]

if __name__ == "__main__":
    result = transcribe("./audio.mp3")
    print(f"result: {result}")

# YouTube videos and shorts summarization service

## Install

**The app was tested on the following configuration:**

- OS:
  - Ubuntu 22
- Python:
  - 3.11.9(64b)
- LLM (AI):
  - OpenAI GPT-4o mini

1. **Download and install Python:**

   - [How to Install Python on Windows](https://www.geeksforgeeks.org/how-to-install-python-on-windows/)
   - [How to Install Python on Linux](https://www.geeksforgeeks.org/how-to-install-python-on-linux/)
   - [How to Download and Install Python on macOS](https://www.geeksforgeeks.org/how-to-download-and-install-python-latest-version-on-macos-mac-os-x/)

2. **Download and install ffmpeg:**
```bash
sudo apt update
sudo apt install ffmpeg
```

3. **Install requirements:**
```bash
pip install -r requirements.txt
```

4. **Set .env file:**

Create .env file in the project directory:
```bash
touch .env
```
Add to it:
```
LLM_API_KEY="YOUR_LLM_API_KEY"
```

5. **Service launch:*

```bash
streamlit run app.py
```

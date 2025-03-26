# YouTube AI Timecodes Generator

This service downloads and preprocesses subtitles from YouTube video, analyzes and summarizes them and then creates timecodes for every major theme in the video. You don't have to create tim

## Install

**The app was tested on the following configuration:**

- OS:
  - Ubuntu 22
- Python:
  - 3.11.9(64b)
- LLM (AI):
  - Gemini-2.0-Flash

**Download and install Python:**

   - [How to Install Python on Windows](https://www.geeksforgeeks.org/how-to-install-python-on-windows/)
   - [How to Install Python on Linux](https://www.geeksforgeeks.org/how-to-install-python-on-linux/)
   - [How to Download and Install Python on macOS](https://www.geeksforgeeks.org/how-to-download-and-install-python-latest-version-on-macos-mac-os-x/)

**Install requirements:**
```bash
pip install -r requirements.txt
```
**Get API key**

Go to [Google AI studio](https://aistudio.google.com), register there if you aren't and push the button *Get API key* in the upper left corner.
Then follow the instructions.


**Set .env file:**

Create .env file in the project directory:
```bash
touch .env
```
Enter your LLM API key in the .env file
```
LLM_API_KEY="YOUR_LLM_API_KEY"
```

# Service launch

1. Run command in bash
```bash
streamlit run app.py
```

2. Browser window will be opened. 

3. Choose subtitles language and enter link to the YouTube.

4. Press *Generate timecodes* button

5. Enjoy the result :)

![alt text](image.png)

# FAQ

**Q**: Is this service free? Do I have to pay for LLM API?

**A**: Yes, it's free. No, you don't have to pay for LLM API. Google has free tier for its API access. The free tier is limited to 15 requests per minute and this limit is more than enough for personal usage of this service.

**Q**: Is the quality of timecodes generation good enough?

**A**: I think it is good, but if you aren't pleased by some of timecodes you can change them after generation as you want. Or you can run multiple generations and select the best result.

**O**: I enter the link to YouTube video, but nothing happens.

**A**: Maybe your YouTube link is incorrect of has timecodes at its end. Check if the video link ends with something like *&t=1s*, delete it and try again.
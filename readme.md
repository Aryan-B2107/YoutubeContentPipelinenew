## YoutubeContentPipelinenew Documentation

 Project Overview
This project is designed to automate parts of a YouTube content creation pipeline. Its primary function is to get long form youtube content, intelligently chunk transcripts, use those chunks as transcripts for short form content. These chunks are again passed through sentiment analysis to score the chunks based on various metrics like shock value, explicit contet, humour score, buildup score, to serially order the extracted videos, easing the content creation process

 Setting Up Your Environment (A Step-by-Step Guide)
To ensure this project runs smoothly on your machine, please follow these steps carefully. This guide covers all necessary prerequisites and configurations.

Prerequisites
Before you begin, make sure you have the following installed on your system:

Python 3.8+

Verify Installation: Open your terminal/command prompt and type: python --version or python3 --version

Download: If not installed, get it from python.org.

pip (Python Package Installer)

Verify Installation: pip --version or pip3 --version

Installation: pip usually comes with Python 3. If not, follow instructions here.

FFmpeg (Crucial for Audio Processing)

FFmpeg is an essential command-line tool for handling multimedia files.

Download: Visit ffmpeg.org/download.html and download the appropriate build for your operating system.

Installation & PATH Setup: This is critical! FFmpeg needs to be accessible from your command line.

Windows:

Download the zip file (e.g., from gyan.dev or btbn.fi).

Extract the zip file to a simple location, like C:\ffmpeg.

Add C:\ffmpeg\bin to your System PATH environment variable.

Search for "Environment Variables" in the Start Menu.

Click "Edit the system environment variables."

Click "Environment Variables..." button.

Under "System variables," find and select Path, then click "Edit...".

Click "New" and add the path to your FFmpeg bin folder (e.g., C:\ffmpeg\bin).

Click "OK" on all windows.

Restart your terminal/command prompt for changes to take effect.

macOS (using Homebrew - Recommended):

brew install ffmpeg

Linux (Debian/Ubuntu):

sudo apt update
sudo apt install ffmpeg

Verify FFmpeg: Open a new terminal/command prompt and type: ffmpeg -version. You should see version information. If not, your PATH setup is incorrect.

Project Setup
Follow these steps to get the project ready to run:

Clone the Repository:

git clone https://github.com/Aryan-B2107/YoutubeContentPipelinenew.git
cd YoutubeContentPipelinenew

Create a Python Virtual Environment (Recommended):
Virtual environments keep your project's dependencies separate from your global Python installation, preventing conflicts.

python -m venv venv

Activate the Virtual Environment:

Windows:

.\venv\Scripts\activate

macOS / Linux:

source venv/bin/activate

(You'll see (venv) or your virtual environment's name appear in your terminal prompt, indicating it's active.)

Install Python Dependencies:
With your virtual environment active, install all required Python packages:

pip install -r requirements.txt

Configure API Keys (.env file):
This project might use external APIs (e.g., Google Gemini for AI analysis). You need to provide your API key securely.

Create a new file named .env in the root directory of your project (the same folder as requirements.txt).

Add your API key(s) in the following format:

GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY_HERE
# Add any other API keys as needed

Replace YOUR_ACTUAL_GEMINI_API_KEY_HERE with your real API key.

Important: Do NOT commit your .env file to GitHub! It's already in the .gitignore to prevent this.

Project Input Files
Main Audio File: Place your primary audio file (e.g., Fluffy Goes To India ｜ Gabriel Iglesias [ux8GZAtCN-M].f251.webm) directly in the project's root directory or update the MAIN_AUDIO_FILE variable in src/audio_processors/audio_mixer.py to point to its correct location.

Transcript Data: The transcript_data (with meme sound assignments) is currently embedded directly within src/audio_processors/audio_mixer.py. In a future iteration, this could be loaded from an external JSON file, which would be more flexible.

Running the Project
Once all the setup steps are complete and your virtual environment is active:

Navigate to the project root:

cd YoutubeContentPipelinenew

Execute the main audio mixing script:

python src/audio_processors/audio_mixer.py

The script will download necessary meme sounds (into a meme_sounds directory) and then process your main audio, outputting final_audio_with_memes.mp3 (or your configured output file name) in the project root.

Troubleshooting Common Issues
ffmpeg -version not found: FFmpeg is not correctly installed or not added to your system's PATH. Revisit Prerequisites Step 3.

ModuleNotFoundError: No module named 'requests' (or similar): You likely forgot to activate your virtual environment or run pip install -r requirements.txt while the environment was active.

UnboundLocalError (or other Python errors): Ensure your Python code is exactly as provided and all dependencies are correctly installed. If you've modified the code, double-check your changes.

"Encoding error" on output MP3: This often means a downloaded meme sound file was corrupted or empty. The script has failsafes to try alternatives, but if it persists, you might need to manually verify the problematic meme sound files in the meme_sounds directory.

API Key Errors: Check your .env file for correct key format and ensure your GEMINI_API_KEY is valid.

 License
This project is licensed under the MIT License - see the LICENSE file for details.


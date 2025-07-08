YoutubeContentPipelinenew
 Project Overview
This project is an automated YouTube content creation pipeline designed to transform long-form video content into engaging short-form clips. Its core functionality involves:

Intelligent Transcript Chunking: Breaking down long video transcripts into logically coherent segments suitable for short-form content.

Sentiment and Content Analysis: Applying sentiment analysis and custom scoring metrics (e.g., shock value, explicit content, humor, buildup) to each extracted chunk.

Serial Ordering: Using these scores to intelligently order the extracted video segments, creating a compelling narrative flow for the final short-form content.

The ultimate goal is to significantly ease the content creation process by automating the identification, analysis, and sequencing of high-impact moments from longer videos.

 Key Capabilities
Long-Form Content Ingestion: Designed to process extended YouTube videos.

Automated Transcript Generation/Processing: Handles the transcript data from the long-form content.

Intelligent Chunking: Divides transcripts into standalone, contextually rich segments.

Advanced Sentiment Analysis: Scores chunks based on various metrics like:

Shock Value

Explicit Content Detection

Humor Score

Buildup Score

Dynamic Ordering: Arranges the extracted short-form video segments based on their analytical scores to optimize viewer engagement.

Automated Audio Mixing (Optional): Integrates meme sound effects at precise timestamps within the processed audio (as seen in audio_mixer.py).

 Pipeline Flow (How It Works)
The pipeline orchestrates several key steps to transform raw long-form content into polished short-form videos:

Input: A long-form YouTube video URL or local video file is provided.

Transcription: The audio from the long-form content is transcribed into a detailed, timestamped text format.

Chunking: The raw transcript is passed through an intelligent chunking module (leveraging LLMs) to identify and extract distinct, self-contained segments suitable for short-form videos.

Analysis & Scoring: Each identified chunk is analyzed using sentiment and content scoring models to assign metrics like humor, shock, buildup, and explicit content scores.

Ordering: Based on the assigned scores and user-defined preferences, the chunks are serially ordered to create an optimal flow for the final short-form video.

Content Assembly: The original video/audio segments corresponding to the ordered chunks are extracted and potentially enhanced (e.g., with meme sound effects via audio_mixer.py).

Output: A ready-to-publish short-form video (or audio) sequence is generated.

⚙️ Setting Up Your Environment (A Step-by-Step Guide)
To ensure this project runs smoothly on your machine, please follow these steps carefully. This guide covers all necessary prerequisites and configurations.

Prerequisites
Before you begin, make sure you have the following installed on your system:

Python 3.8+

Verify Installation: Open your terminal/command prompt and type: python --version or python3 --version

Download: If not installed, get it from python.org.

pip (Python Package Installer)

Verify Installation: pip --version or pip3 --version

Installation: pip usually comes with Python 3. If not, follow instructions here.

FFmpeg (Crucial for Audio/Video Processing)

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
This project heavily relies on external APIs (e.g., Google Gemini for AI analysis, potentially YouTube Data API for video fetching). You need to provide your API key(s) securely.

Create a new file named .env in the root directory of your project (the same folder as requirements.txt).

Add your API key(s) in the following format:

GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY_HERE
YOUTUBE_API_KEY=YOUR_YOUTUBE_DATA_API_KEY_HERE # Example for YouTube API
# Add any other API keys as needed

Replace YOUR_ACTUAL_GEMINI_API_KEY_HERE and any other placeholder keys with your real API keys.

Important: Do NOT commit your .env file to GitHub! It's already in the .gitignore to prevent this.

Project Input & Configuration
YouTube Content: The pipeline is designed to work with long-form YouTube content. You will likely specify the YouTube video ID or URL as an input to the main script.

Transcript Data: While audio_mixer.py currently embeds transcript data, the full pipeline would dynamically fetch or generate transcripts from the input video.

Meme Sound Configuration: The meme_sounds directory will be created to store downloaded sound effects. The mapping for these sounds is handled internally by the audio_mixer.py script.

🏃‍♀️ Running the Project (Modular Execution)
Once all the setup steps are complete and your virtual environment is active, you can execute the different stages of the pipeline. You can run these modules individually or integrate them into a larger orchestration script (e.g., main_pipeline.py if you create one).

Navigate to the project root:

cd YoutubeContentPipelinenew

Stage 1: Transcription (e.g., src/transcribers/transcriber.py)
This module is responsible for obtaining or generating the transcript of your long-form content.
(Assumed usage based on module name)

python src/transcribers/transcriber.py --video_url "YOUR_YOUTUBE_VIDEO_URL" --output_json "path/to/output_transcript.json"

--video_url: The URL of the YouTube video to transcribe.

--output_json: The path where the generated timestamped transcript JSON will be saved.

Stage 2: Transcript Analysis & Chunking (e.g., src/transcript_analysers/analyzer.py)
This module takes the raw transcript, intelligently chunks it, performs sentiment/content analysis, and orders the segments.
(Assumed usage based on module name)

python src/transcript_analysers/analyzer.py --input_transcript "path/to/output_transcript.json" --output_chunks "path/to/analyzed_chunks.json" --prompt_type "jokes" # or "tech"

--input_transcript: Path to the JSON transcript generated in Stage 1.

--output_chunks: Path where the analyzed and chunked JSON (with scores and ordering) will be saved.

--prompt_type: Specifies the type of analysis (e.g., "jokes" or "tech") as defined in your LLM prompts.

Stage 3: Audio Mixing (e.g., src/audio_processors/audio_mixer.py)
This module takes your main audio and overlays meme sound effects based on timestamps.
(Assumed usage based on module name and previous discussions)

python src/audio_processors/audio_mixer.py --main_audio "path/to/main_audio.webm" --meme_config "path/to/analyzed_chunks.json" --output_audio "path/to/final_audio_with_memes.mp3"

--main_audio: Path to your primary audio file (e.g., downloaded from YouTube).

--meme_config: Path to the analyzed chunks JSON from Stage 2, which should contain the meme sound assignments and timestamps.

--output_audio: The desired path for the final mixed audio file.

Stage 4: Video Assembly (Future/Placeholder)
This stage would involve taking the original video segments corresponding to the ordered chunks and combining them with the mixed audio to produce the final short-form video.
(This module is not yet implemented in your provided code, but is part of your project overview.)

# Example: python src/video_assembler/assembler.py --video_source "original_video.mp4" --chunk_order "path/to/analyzed_chunks.json" --mixed_audio "path/to/final_audio_with_memes.mp3" --final_output "short_form_video.mp4"

Troubleshooting Common Issues
ffmpeg -version not found: FFmpeg is not correctly installed or not added to your system's PATH. Revisit Prerequisites Step 3.

ModuleNotFoundError: No module named 'requests' (or similar): You likely forgot to activate your virtual environment or run pip install -r requirements.txt while the environment was active.

Python Errors (UnboundLocalError, etc.): Ensure your Python code is exactly as provided and all dependencies are correctly installed. If you've modified the code, double-check your changes.

"Encoding error" on output MP3/MP4: This can indicate issues with FFmpeg, corrupted input files (including downloaded meme sounds), or incorrect FFmpeg command parameters. The audio_mixer.py has failsafes for meme downloads, but if it persists, you might need to manually verify source files or FFmpeg logs for more details.

API Key Errors: Check your .env file for correct key format and ensure your GEMINI_API_KEY (and any other API keys) are valid and have the necessary permissions.


This project is licensed under the MIT License - see the LICENSE file for details.


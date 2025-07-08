import os
import json
import sys
import subprocess
import time
import threading

import google.genai.errors

from transcribers import transcript_filter, joke_joiner
from transcript_analyzers import LLM1_transcript_chunking, LLM2_chunked_transcript_scorer, transcript_sorter
from dotenv import load_dotenv

#This is an entry point class
load_dotenv()


# Add this right after load_dotenv()
base_path = os.getenv("BASE_PATH")

# Function to expand BASE_PATH in environment variables
def expand_base_path(path):
    if path and '%BASE_PATH%' in path:
        return path.replace('%BASE_PATH%', base_path)
    return path

# Fix the timestamped variable name (it was lowercase in the code but uppercase in env)
api_key = os.getenv("API_KEY")
raw_trnscrpt = expand_base_path(os.getenv("RAW_TRANSCRIPT_PATH"))
convert_json = expand_base_path(os.getenv("CONVERT_TRANSCRIPT_JSON"))
joined_jokes = expand_base_path(os.getenv("JOIN_JOKES"))
joke_seg = expand_base_path(os.getenv("JOKE_SEGMENTS"))
timestamped = expand_base_path(os.getenv("TIMESTAMPED_PATH"))  # Fixed variable name
parameter_chunk_path = expand_base_path(os.getenv("PARAMETER_CHUNK_PATH"))
scored_segment_path = expand_base_path(os.getenv("SCORED_SEG_PATH"))


def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

import itertools

import sys
import time

import sys
import time

stop_spinner = False
progress = 0.0


def spinner(message="Processing", bar_length=70):
    global progress
    while not stop_spinner or progress < 100:
        if progress < 100:
            progress += 0.2  # very smooth increments
            if progress > 100:
                progress = 100
        filled_length = int(bar_length * progress / 100)
        bar = '|' * filled_length + ' ' * (bar_length - filled_length)
        sys.stdout.write(f'\r{message}... [{bar}] {int(progress):3d}%')
        sys.stdout.flush()
        time.sleep(0.02)  # faster refresh for smoothness
    # Final output line
    sys.stdout.write(f'\r{message}... [{"|" * bar_length}] 100%\n')
    sys.stdout.write('API Call completed Successfully!\n')
    sys.stdout.flush()




if __name__ == "__main__":

    # 1) Raw Transcript is passed through transcript filter to get JSON representation
    try:
        with open(raw_trnscrpt, "r", encoding="utf-8") as file:
            sample_raw_transcript = file.read()
    except FileNotFoundError:
        print("raw_transcript.txt not found.")
        sample_raw_transcript = None

    if sample_raw_transcript:
        json_output = transcript_filter.convert_rawtranscript_to_json(sample_raw_transcript)

        try:
            with open(convert_json, 'w', encoding='utf-8') as f:
                json.dump(json_output, f, indent=4, ensure_ascii=False)

            print(json.dumps(json_output, indent=4))

            print(f"{os.path.basename(raw_trnscrpt)} processed successfully and stored in {os.path.basename(convert_json)}")
        except Exception as e:
            print(f"Error {e} occured while processing trancsript")

    # 2) LLM2 Pass which converts the entire







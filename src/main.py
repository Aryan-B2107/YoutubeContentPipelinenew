import os
import json
import sys
import subprocess
import time
import threading

import google.genai.errors

import transcribers
from video_extractor import clip_extractor
from transcribers import transcript_filter, joke_joiner
from transcript_analyzers import LLM1_transcript_chunking, LLM2_chunked_transcript_scorer, transcript_sorter

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
videos_dir = expand_base_path(os.getenv("VIDEOS_DIR"))


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


def simple_spinner():
    char = ''
    spinner_chars = []
    for i in range(10):
        char += '.'
        spinner_chars.append(char)
    i = 0
    while True:
        sys.stdout.write('\r' + ' Loading' + spinner_chars[i % len(spinner_chars)])
        sys.stdout.flush()
        time.sleep(0.3)
        i += 1


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

            print(
                f"{os.path.basename(raw_trnscrpt)} processed successfully and stored in {os.path.basename(convert_json)}")
        except Exception as e:
            print(f"Error {e} occured while processing trancsript")

    # 2) LLM2 Pass which converts the entire

    try:
        print(f"Processing {os.path.basename(convert_json)} and storing in {os.path.basename(joke_seg)}...")

        joke_segments = LLM1_transcript_chunking.chunk_jokes(convert_json, api_key)
        print(joke_segments)
        print("Transcript chunked successfully")
        print(f"Writing segments in {os.path.basename(joke_seg)}")

        with open(joke_seg, 'w') as f:
            json.dump(joke_segments, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error occurred while chunking transcript data: {e}")

    # joke_joiner.py is called to prepare data chunks, to send to llm2 pass

    INPUT_FILE1 = convert_json
    INPUT_FILE2 = joke_seg
    print(convert_json)
    print(INPUT_FILE2)
    # Read and parse JSON files
    try:
        with open(INPUT_FILE1, 'r', encoding='utf-8') as f:
            transcript_segments = json.load(f)

        with open(INPUT_FILE2, 'r', encoding='utf-8') as f:
            joke_data = json.load(f)
            joke_chunks = joke_data['chunks']  # Extract the chunks array

        # Call function once and unpack results
        joined, content_timestamp_dict = joke_joiner.process_jokes(transcript_segments, joke_chunks)

        print(joined)
        print(content_timestamp_dict)

        with open(joined_jokes, 'w', encoding='utf-8') as f:
            json.dump({"jokes": joined}, f, indent=2, ensure_ascii=False)
        with open(timestamped, 'w', encoding='utf-8') as f:
            json.dump(content_timestamp_dict, f, indent=2, ensure_ascii=False)

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
    except Exception as e:
        print(f"Error: {e}")

    # LLM2 Pass which parses and parameterizes the data, preparing it for scoring, and finlly makes call to the service

    LLM2_chunked_transcript_scorer.parse_and_parameterize(joined_jokes, parameter_chunk_path)
    scored_segs = LLM2_chunked_transcript_scorer.score_chunks(parameter_chunk_path, api_key)

    #Runing the Transcript_sorter, sorting clips as per score

    reordered_timestamped = transcript_sorter.main()
    print(reordered_timestamped)
    with open(timestamped, 'w') as f:
        json.dump(reordered_timestamped, f, indent=2, ensure_ascii=False )

    #Extracting clips from long video, using the order tht transcript sorter actually made

    base_path = os.getenv("BASE_PATH")

    # Configure other paths relative to BASE_PATH
    print(videos_dir + "final_segmented_clips")
    input_vid = os.path.join(videos_dir, "fluffy_output.mp4")
    output_location = videos_dir + "final_segmented_clips"
    ffmpeg_path = videos_dir + "ffmpeg.exe"

    os.makedirs(videos_dir, exist_ok=True)


    clip_extractor.clippingFromVideo(timestamped, input_vid, output_location, ffmpeg_path)
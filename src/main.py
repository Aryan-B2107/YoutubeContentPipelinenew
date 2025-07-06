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
# Create required directories before any file operations
required_dirs = [
    os.path.dirname(p) for p in [
        raw_trnscrpt,
        convert_json,
        joined_jokes,
        joke_seg,
        timestamped,
        parameter_chunk_path,
        scored_segment_path
    ] if p is not None
]

# Add video-related directories
required_dirs.extend([
    os.path.join(base_path, "data", "transcripts"),
    os.path.join(base_path, "data", "videos"),
    os.path.join(base_path, "data", "videos", "final_segmented_clips")
])

# Create all required directories
for directory in required_dirs:
    if directory:
        os.makedirs(directory, exist_ok=True)

# Update video processing paths to use base_path
input_file = os.path.join(base_path, "data", "transcripts", "timestamped_collection.json")
input_vid = os.path.join(base_path, "data", "videos", "fluffy_output.mp4")
output_loc = os.path.join(base_path, "data", "videos", "final_segmented_clips")
ffmpeg_path = os.path.join(base_path,"data", "videos", "ffmpeg.exe")




stop_spinner = False  # module-level flag to control spinner thread


def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


import itertools

import sys
import time

progress = 0

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

        with open(convert_json, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=4, ensure_ascii=False)

        print(json.dumps(json_output, indent=4))

    # 2) LLM1 Pass which chunks the jokes as per appropriate guidelines

    """if sample_raw_transcript:
        # Start spinner in separate thread
        stop_spinner = False
        spinner_thread = threading.Thread(target=spinner, args=("Chunking transcript",))
        spinner_thread.start()

        try:
            segments = LLM1_transcript_chunking.chunk_jokes(convert_json, api_key)
            # reload joke_seg path in case env updated
            joke_seg = os.getenv("JOKE_SEGMENTS")
            save_json(segments, joke_seg)

        except FileNotFoundError:
            print("Converted_transcript.json not found.")
        except Exception as e:
            print(f"Error during chunking: {e}")

        # Stop spinner and wait for thread to finish
        stop_spinner = True
        spinner_thread.join()"""

    # 3) Join jokes as per LLM1 generated timestamps

    """try:
        joke_joiner.run_pipeline(
            transcript_path=convert_json,
            jokes_path=joke_seg,
            output_jokes_path=joined_jokes,
            output_timestamps_path=timestamped
        )
    except FileNotFoundError:
        print("Files not found.")

    # 4) LLM 2 scores takes in joined_jokes.json input, and returns a scored json for every joke

    #Parse and parameterize:
    LLM2_chunked_transcript_scorer.parse_and_parameterize(joined_jokes, parameter_chunk_path)

    try:
        scored_segments = LLM2_chunked_transcript_scorer.score_chunks(parameter_chunk_path, api_key)
        with open(scored_segment_path, 'w', encoding='utf-8', errors='ignore') as file:
            json.dump(scored_segments, file, indent=2)
    except google.genai.errors.ClientError as e:  # Log the error but continue execution
        print(f"Google GenAI Client Error: {str(e)}. Continuing with the next steps...")"""



    # 5) sort the transcripts the bottom line doesn't work! individually running transcript sorter works, but
    reordered_timestamped = transcript_sorter.main()
    print(reordered_timestamped)
    with open(timestamped, "w") as f:
        json.dump(reordered_timestamped, f, indent=2)

    # 6) Clipping from video:
    def normalize_time(t):
        """Convert M:SS or MM:SS to HH:MM:SS format."""
        parts = t.split(":")
        if len(parts) == 2:
            minutes, seconds = parts
            hours = 0
        elif len(parts) == 3:
            hours, minutes, seconds = parts
        else:
            raise ValueError(f"Invalid time format: {t}")

        total_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        return total_time



    #
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error Loading file:{input_file}")

    os.makedirs(output_loc, exist_ok=True)

    try:
        counter = 0
        for content_id, times in data.items():
            start = normalize_time(times['start_time'])
            end = normalize_time(times['end_time'])
            counter += 1
            char = ''
            for i in range(len(content_id)):
                char += content_id[i].upper()
                if content_id[i] == "_":
                    break

            output_file = os.path.join(output_loc, f"{char}_ID{counter}.mp4")

            #commands:
            cmd = [
                ffmpeg_path,
                '-ss', start,
                '-to', end,
                '-i', input_vid,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-strict', 'experimental',
                output_file
            ]
            print(f"Extracting {content_id} from ({start} to {end} -> {output_file})")
            subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error extracting files")
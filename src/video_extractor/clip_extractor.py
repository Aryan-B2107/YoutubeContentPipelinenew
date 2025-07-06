
import json
import os
import subprocess
from dotenv import load_dotenv

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


def clippingFromVideo(input_file, input_vid, output_loc, ffmpeg_path):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error Loading file:{input_file}")
        return

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
        print(f"Error extracting files: {e}")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Get base path and expand it in other paths
    base_path = os.getenv("BASE_PATH")

    # Get timestamped path from env and expand BASE_PATH
    timestamped_path = os.getenv("TIMESTAMPED_PATH").replace("%BASE_PATH%", base_path)

    # Configure other paths relative to BASE_PATH
    videos_dir = os.path.join(base_path, "data", "videos")
    input_vid = os.path.join(videos_dir, "fluffy_output.mp4")
    output_location = os.path.join(videos_dir, "final_segmented_clips")
    ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")

    # Create videos directory if it doesn't exist
    os.makedirs(videos_dir, exist_ok=True)

    clippingFromVideo(timestamped_path, input_vid, output_location, ffmpeg_path)
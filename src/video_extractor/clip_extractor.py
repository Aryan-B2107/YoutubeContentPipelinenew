r"""
This extractor uses reference of; D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcribers\timestamped_collection.json

 to extract clips from downloaded video inside:
 D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\Fluffy Goes To India ｜ Gabriel Iglesias [ux8GZAtCN-M].mp4

and outputs final clips inside:
D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\final_segmented_clips
"""

import json
import os
import subprocess

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


def clippingFromVideo(input_file, input_vid, output_loc):
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
                r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\ffmpeg.exe",
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


if __name__ == "__main__":
    file = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcribers\timestamped_collection.json"
    vid = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\output.mp4"
    output_location = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\final_segmented_clips"


    clippingFromVideo(file, vid, output_location)
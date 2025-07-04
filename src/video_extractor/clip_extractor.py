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

    for content_id, times in data.items():
        start = times['start_time']
        end = times['end_time']



if __name__ == "__main__":
    file = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcribers\timestamped_collection.json"
    vid = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\Fluffy Goes To India ｜ Gabriel Iglesias [ux8GZAtCN-M].mp4"
    output_location = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\final_segmented_clips"

    clippingFromVideo(file, vid, output_location)
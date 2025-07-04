r"""
This extractor uses reference of; D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcribers\timestamped_collection.json

 to extract clips from downloaded video inside:
 D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\Fluffy Goes To India ｜ Gabriel Iglesias [ux8GZAtCN-M].mp4

and outputs final clips inside:
D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\final_segmented_clips
"""

import json
import subprocess

def clippingFromVideo(input_file, input_vid, output_loc):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error Loading file:{input_file}")

    for


if __name__ == "__main__":
    file = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcribers\timestamped_collection.json"
    vid = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\Fluffy Goes To India ｜ Gabriel Iglesias [ux8GZAtCN-M].mp4"
    output_location = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\videos\final_segmented_clips"

    clippingFromVideo(file, vid, output_location)
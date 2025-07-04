import json
import os
from datetime import datetime, timedelta


def time_to_seconds(time_str):
    """Convert time string (MM:SS or H:MM:SS) to seconds"""
    if time_str is None:
        return 0  # Default to 0 seconds if time is None

    if not isinstance(time_str, str):
        return 0  # Default to 0 seconds if not a string

    parts = time_str.split(':')
    if len(parts) == 2:  # MM:SS format
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:  # H:MM:SS format
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")


def is_time_in_range(segment_start, segment_end, joke_start, joke_end):
    """Check if a transcript segment overlaps with a joke time range"""
    # Convert all times to seconds for comparison
    seg_start_sec = time_to_seconds(segment_start)
    seg_end_sec = time_to_seconds(segment_end)
    joke_start_sec = time_to_seconds(joke_start)
    joke_end_sec = time_to_seconds(joke_end)

    # Check if there's any overlap between the segments
    return not (seg_end_sec <= joke_start_sec or seg_start_sec >= joke_end_sec)


def load_json_file(filepath):
    """Load and return JSON data from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        return None






def main():
    # Define file paths
    base_dir = "src"
    transcript_file = r'Converted_json_transcript.json'
    jokes_segments_file = r'D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcript_analyzers\joke_segments.json'
    output_file = "joined_jokes.json"

    # Load the transcript data
    print("Loading transcript data...")
    transcript_data = load_json_file(transcript_file)
    if transcript_data is None:
        return

    # Load the jokes segments data
    print("Loading jokes segments data...")
    jokes_data = load_json_file(jokes_segments_file)
    if jokes_data is None:
        return

    # Extract transcript segments and joke chunks
    transcript_segments = transcript_data if isinstance(transcript_data, list) else transcript_data.get('segments', [])
    joke_chunks = jokes_data.get('chunks', [])

    print(f"Found {len(transcript_segments)} transcript segments")
    print(f"Found {len(joke_chunks)} joke chunks")

    # Process each joke chunk
    joined_jokes = []
    count = 0

    content_timestamp_dict = {}

    for i, chunk in enumerate(joke_chunks):
        print(f"Processing joke chunk {i + 1}/{len(joke_chunks)}: {chunk['start_time']} - {chunk['end_time']}")

        joke_start = chunk['start_time']
        joke_end = chunk['end_time']

        key = f"Content_ID{i}"
        content_timestamp_dict[key] = {
            'start_time': joke_start,
            'end_time': joke_end
        }

        # Find all transcript segments that fall within this joke's time range
        matching_segments = []

        for segment in transcript_segments:
            segment_start = segment.get('start_time')
            segment_end = segment.get('end_time')

            # Skip segments with missing time data
            if segment_start is None or segment_end is None:
                continue

            if is_time_in_range(segment_start, segment_end, joke_start, joke_end):
                matching_segments.append(segment)

        # Sort matching segments by start time to maintain order
        matching_segments.sort(key=lambda x: time_to_seconds(x['start_time']))

        # Join the content with spaces
        joke_content = ' '.join(segment['content'] for segment in matching_segments)

        if joke_content.strip():  # Only add if there's actual content
            count += 1
            joined_jokes.append({
                f"content_ID{count}": joke_content.strip()
            })
            print(f"  → Found {len(matching_segments)} matching segments")
        else:
            print(f"  → No matching content found for this time range")

    # Create the output structure
    output_data = {
        "jokes": joined_jokes
    }

    # Save to file
    print(f"\nSaving {len(joined_jokes)} jokes to {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"Successfully created {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")

    print(content_timestamp_dict)

    # Save to file(contentID : timestamps)
    try:
        with open('timestamped_collection.json', 'w') as file:
            json.dump(content_timestamp_dict, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving file: {e}")


# We have joined the jokes, but we disregarded timestamp data to reduce input size, although we still need it to
# extract video clips from the YouTube video
# into timestamped_collection.json, where I grab the timestamps, create this json, where we have content_ID and timestamps
# which represent that contentID



if __name__ == "__main__":
    main()
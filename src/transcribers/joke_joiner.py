import json
import os

from dotenv import load_dotenv

#This is an entry point class
load_dotenv()

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

def time_to_seconds(time_str):
    if time_str is None or not isinstance(time_str, str):
        return 0

    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")


def is_time_in_range(segment_start, segment_end, joke_start, joke_end):
    seg_start_sec = time_to_seconds(segment_start)
    seg_end_sec = time_to_seconds(segment_end)
    joke_start_sec = time_to_seconds(joke_start)
    joke_end_sec = time_to_seconds(joke_end)

    return not (seg_end_sec <= joke_start_sec or seg_start_sec >= joke_end_sec)


def process_jokes(transcript_segments, joke_chunks):
    joined_jokes = []
    content_timestamp_dict = {}
    count = 0

    for i, chunk in enumerate(joke_chunks):
        print(f"Processing joke chunk {i + 1}/{len(joke_chunks)}: {chunk['start_time']} - {chunk['end_time']}")

        joke_start = chunk['start_time']
        joke_end = chunk['end_time']
        key = f"Content_ID{count + 1}"

        content_timestamp_dict[key] = {
            'start_time': joke_start,
            'end_time': joke_end
        }

        matching_segments = []
        for segment in transcript_segments:
            seg_start = segment.get('start_time')
            seg_end = segment.get('end_time')
            if seg_start is None or seg_end is None:
                continue
            if is_time_in_range(seg_start, seg_end, joke_start, joke_end):
                matching_segments.append(segment)

        matching_segments.sort(key=lambda x: time_to_seconds(x['start_time']))
        joke_content = ' '.join(segment['content'] for segment in matching_segments if 'content' in segment)

        if joke_content.strip():
            count += 1
            joined_jokes.append({f"content_ID{count}": joke_content.strip()})
            print(f"  → Found {len(matching_segments)} matching segments")
        else:
            print(f"  → No matching content found for this time range")

    return joined_jokes, content_timestamp_dict


if __name__ == "__main__":
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
        joined, content_timestamp_dict = process_jokes(transcript_segments, joke_chunks)


        print(joined)
        print(content_timestamp_dict)

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
    except Exception as e:
        print(f"Error: {e}")
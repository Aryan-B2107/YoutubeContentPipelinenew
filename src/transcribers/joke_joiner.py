import json
import os


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


def load_json_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        return None


def save_json_file(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved file: {filepath}")
    except Exception as e:
        print(f"Error saving file {filepath}: {e}")


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


def run_pipeline(
    transcript_path,
    jokes_path,
    output_jokes_path,
    output_timestamps_path
):
    print("Loading transcript data...")
    transcript_data = load_json_file(transcript_path)
    if not transcript_data:
        return

    print("Loading jokes data...")
    jokes_data = load_json_file(jokes_path)
    if not jokes_data:
        return

    transcript_segments = transcript_data if isinstance(transcript_data, list) else transcript_data.get('segments', [])
    joke_chunks = jokes_data.get('chunks', [])

    print(f"Found {len(transcript_segments)} transcript segments")
    print(f"Found {len(joke_chunks)} joke chunks")

    joined_jokes, timestamps = process_jokes(transcript_segments, joke_chunks)

    save_json_file({"jokes": joined_jokes}, output_jokes_path)
    save_json_file(timestamps, output_timestamps_path)

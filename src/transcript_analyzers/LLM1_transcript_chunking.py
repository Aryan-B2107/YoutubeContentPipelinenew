"""
1) entering API KEY:
headers = {
    'Authorization': 'AIzaSyCSeMpywZGvLDIgYi67_vvlm_S---Ioabg',
    'Content-Type': 'application/json'
}

2)Request Format:
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": "Summarize this transcript: [your transcript here]"
    }
  ],
  "max_tokens": 500,
  "temperature": 0.7
}

3) Result Format
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here's a summary of the transcript..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "total_tokens": 150
  }

"""

#Final Desired OUTPUT FORMAT EXAMPLE:

"""chunks: [
    {
      "start_time": "00:05:23",
      "end_time": "00:06:45",
      "type": "joke",
      "content": "So I went to the doctor..."
    },
    {
      "start_time": "00:12:10",
      "end_time": "00:13:02",
      "type": "joke",
      "content": "My wife told me to stop singing..."
    }
  ]
"""

SYSTEM_PROMPT = """SYSTEM_PROMPT = 
You are a content segmentation expert. Analyze this timestamped transcript to identify complete standalone segments.

TASK: Identify Standalone segments that would individually work as short videos

IDENTIFY complete segments by looking for:
- Setup: Context/premise establishment
- Natural Pauses: Breathing room
- Complete statements or stories
- Build-up: Tension/anticipation building
- Punchline: Comedic payoff
- Reaction: Audience laughter/response (if present)
- Optional: question - answer pairs
- Lists or examples that finish

RULES:
- A complete joke MUST include setup + punchline + optional(Audience laughter/praise more than once for longer segments)
- Don't split jokes mid-delivery
- Optional - Prioritise explicit content containing derived references, culture shock
- Include natural pauses/reactions as part of the joke unit
- Don't cut mid-sentence or mid thought or examples being explained
- Identify natural entry and exit points which would serve the context(can bypass this rule if amount of segments found are too low)
- each chunk should make sense without additional context(can bypass this rule if amount of segments found are too low)


INPUT FORMAT: Array of {content, start_time, end_time}

While Identifying start_time and end_time, refer to the Rules and Identifications declared above
DO NOT cut in between delivery
 OUTPUT FORMAT:
{
  "chunks": [
    {
      "Title":"Lists in Python"
      "start_time": "1:23",
      "end_time": "1:45",
      "duration": "0:22",
    }
  ]
}

"""

"""
You are a content segmentation expert.
Analyze the following timestamped transcript to extract concise, topically complete segments of content specifically related to technology. These segments will be repurposed as independent clips for short-form educational and archival usage.

TASK:
Identify and return standalone, topic-complete segments that contain logically complete technical information, and optionally include intro and outro segments as independent structural units.

SEGMENT TYPES TO IDENTIFY:
Main Technology Segments — Focused technical discussions or explanations

Intro Segment — Includes greetings, episode/topic introductions, guest intro, or format briefing

Outro Segment — Includes thanks, closing remarks, calls to action, or sign-offs

TECHNOLOGY CONTENT CRITERIA:
A segment is technology-related if it involves discussion of:

Programming, development, languages, tools

AI, ML, NLP, Data Engineering

Cybersecurity, blockchain, cryptography

Cloud, infrastructure, automation, APIs

DevOps, CI/CD, containers, orchestration

Robotics, hardware, VLSI, embedded systems

Consumer electronics, product engineering, chip design

Tech careers, educational content, system design

Exclude motivational content, personal anecdotes, or general humor unless it's directly used to explain a technical idea.

STRUCTURAL SEGMENTATION RULES:
Each segment must:

Begin at a topic setup, transition, or clear pause

End with a topic conclusion, wrap-up, or natural shift

Be logically self-contained (exception allowed for sparse input)

NOT split examples, explanations, or multi-part arguments

NOT cut mid-sentence, mid-concept, or between list items

In the middle of code or config explanations
While Identifying start_time and end_time, refer to the Rules and Identifications declared above
DO NOT cut in between delivery
 OUTPUT FORMAT:
{
  "chunks": [
    {
      "Title":"Lists in Python"
      "start_time": "1:23",
      "end_time": "1:45",
      "duration": "0:22",
    }
  ]
}


"""
#Manually add chunk_id key value pair to above chunk format


from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


# change kar api key chi location, save it in that, thing i don't remember now, so that it can't be accessed


#NOTE: Initially we have to limit to content extraction form 20 minute videos. because of 8000 output token limits
def chunk_jokes(transcript_json_file, api_key):
    """
    This Function takes in input JSON file of transcript data,
    and converts it to relevant widths of short clip content

    :param transcript_json_file: JSON input generated by transcript filter
    :param api_key: CONFIDENTIAL
    :return: JSON output in specified format
    """
    #Setting up new SDK
    client = genai.Client(api_key=api_key)

    #Load Transcript
    with open(transcript_json_file, 'r', encoding='utf-8') as f:
        transcript_data = json.load(f)

    #fetch prompt
    prompt = f"""
    {SYSTEM_PROMPT}
    
    Transcript to Analyse:
    {json.dumps(transcript_data, indent=2)}
    
    RETURN only the JSON response in the SPECIFIED FORMAT
    """
    generation_config = {
        'temperature': 0.2,
        'top_p': 0.9,
        'top_k': 20,
        'max_output_tokens': 4096,
        'response_mime_type': 'application/json'
    }
    #Generate
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config=generation_config
    )

    #Save into new file, return

    segments = json.loads(response.text)
    with open('joke_segments.json', 'w') as f:
        json.dump(segments, f, indent=2)
    print(segments)
    return segments

if __name__ == "__main__":
    chunk_jokes(r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcribers\Converted_json_transcript.json", api_key)

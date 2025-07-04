"""
Initially for the sake of working, I'm going to fetch the transcript using YouTubeTranscriptApi.

But Eventually the following will be implemented:
1)Use Beautiful soup to get html of a give YouTube URL
2)scrape the relevant transcript part through analysing css formats, getting all the relevant data like
time stamps and the transcript for that time stamp
3) write in a clean json file and return the json file

"""
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

video_id = "MrpLH-MlICY"





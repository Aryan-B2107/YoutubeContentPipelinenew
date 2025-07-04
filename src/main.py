from transcribers import transcript_filter
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

if __name__ == "__main__":
    transcript_filter.main()



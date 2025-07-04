"""
This pass will:

1)check completeness of joke
and correctness of other metrics
2)will also make more parameters in the joined_jokes.json:

Initially I'm Implementing this with a simplified workflow which makes the llm return the entire scored json again.

The future goal is to parse and tokenise the json objects, and ask the model individual elements, such that input
prompt length isn't unnecessarily too long with elements  like ('humour_score', 'shock value', 'buildup_score ')
"""

import json
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def parse_and_parameterize(input_file, output_file):
    """
    This function takes in the input json file from joined jokes.json, which is a collection of the segments collected
    And parses the json file to add more parameters based on which segment will be scored by API call
    :return:
    """
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)
            print(f"Successfully loaded data form the '{input_file}'.")
            for i in range(len(data['jokes']) - 12): # minus 8 is just for rapid testing on a realistic range
                data['jokes'][i]['humour_score'] = 0.0
                data['jokes'][i]['shock_value'] = 0.0
                #data['jokes'][i]['explicit_content_score'] = 0.0
            print(data)
            with open("parameterized_chunks.json", 'w') as file:
                json.dump(data, file, indent=2)

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not loaded.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file '{input_file}' is not a valid json file")
        return


SYSTEM_PROMPT = """ You are a joke analysis expert. 
Your job is to analyse the CONTENT parameter of the individual json objects from the input json in the following format:

INPUT FORMAT:
{
  "jokes": [
    {
      "content_ID1": "Martina and I just got back from India yeah so let me tell you I started posting on Facebook and Twitter that we were gonna go out there to do these shows and then people started sending me messages questioning what I was gonna do first of all are they gonna understand you in India will they understand English okay will they be able to follow along with your stories once we got there I come to find out that more people speak English in India than in all of the u.s. and Canada put together might as well throw Mexico in there for extra credit because there's that many people and yes they have the internet they got the Internet they got Bollywood they got Hollywood they understand American culture so much more than we understand theirs second thing people tried to warn me about going over there Gabriel be careful India is a third-world country don't drink the water in India it contains parasites that'll make you really sick don't eat the food from the street people especially the street meat it contains a parasite that'll make you really sick and most importantly there's a lot of crime over there don't stay out late when the Sun Goes Down I'm like is it that bad so I'm like let me get this straight there's a lot of crime don't stay out late don't eat any of the food from the street vendors and don't drink the water why does that sound familiar that's Mexico",
      "humour_score": 0.0,
      "shock_value": 0.0,

      
    },
    {
      "content_ID2": "when Martina and I got over there we found out that Indian people and Mexican people have so much in common you guys I'm telling you it's insane how similar we are especially the food the food is so similar for example Mexicans love tortillas Indian people love naan bread which is a fluffier form of a tortilla Mexicans love chicken Indians love chicken Mexicans love hot and spicy Indians invented hot and spicy most popular drink in Mexico is Fanta most popular drink in India is Fanta Indian people worship cows Mexicans love barbecues a lot of similarities most of",
      "humour_score": 0.0,
      "shock_value": 0.0,

      
    },
    {
      "content_ID3": "the people that I met over there were very hard-working and humble and I got to tell you every time I talk to someone I was always greeted the same way they look at me they put their hands together they do a little bow and they say namaste which is an endearing hello it's really nice and sweet and then I noticed that Indian people when you're talking to them do this thing with their head or it will begin to move side to side as they're speaking now first when you notice that you think oh he slept wrong he just got a kink in his neck get a",
      "humour_score": 0.0,
      "shock_value": 0.0,

      
    }
  ]
} 

The analysis has to be done following the <RULES>

<RULES>
ALL SCORES SHOULD BE IN FLOAT RANGE (0 to 10)

Shock Value Score:
Measures how unexpected the peak was
Measures how surprising, controversial, or taboo the joke is, often enhancing its viral potential.

Explicit Content Score:
Rates the level of profanity, sexual references, or culturally sensitive material in the joke.

The Humour Score captures the overall comedic impact of a segment by considering several blended elements
including how funny the content is perceived to be, the timing and delivery of the punchline, the cleverness or 
absurdity of the setup

<\RULES>

And  give output in the following format strictly following <RULES>:
RETURN ONLY JSON FORMAT
DO NOT ADD TEXT BEFORE OR AFTER JSON
{
  "jokes": [
    {
      "content_IDN": "...",
      "humour_score": "...",
      "shock_value": "...",

      
    }
  ]
}

"""

def score_chunks(parameterized_json, api_key):

    #setting client
    client = genai.Client(api_key=api_key)

    # Load Transcript
    with open(parameterized_json, 'r', encoding='utf-8') as f:
        parameterized_data = json.load(f)

    #fetch prompt
    prompt = f"""
    {SYSTEM_PROMPT}
    JSON TO ANALYSE:
    {json.dumps(parameterized_data, indent=2)}
    
    RETURN only the JSON response in the SPECIFIED FORMAT
"""
    generation_config = {
        'temperature': 0.2,
        'top_p': 0.9,
        'top_k': 20,
        'max_output_tokens': 8000,
        'response_mime_type': 'application/json'
    }
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config= generation_config
    )
    print(response.text)
    scored_segments = json.loads(response.text)



    with open('scored_chunks.json', 'w') as file:
        json.dump(scored_segments, file, indent=2)
    print(scored_segments)
    return scored_segments

if __name__ == "__main__":
    input_json = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcribers\joined_jokes.json"
    output_json = "parameterized_chunks.json"
    parse_and_parameterize(input_json, output_json)
    try:
        score_chunks('parameterized_chunks.json', api_key)
        print("successfully fetched output from gemini api and stored in scored_chunks.json")
    except Exception:
        print("Token Limit reached, output not completed")

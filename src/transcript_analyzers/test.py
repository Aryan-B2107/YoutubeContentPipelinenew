import json
input_file = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcribers\joined_jokes.json"

with open(input_file, 'r') as file:
    data = json.load(file)

score_types = ["humour_score", 'shock_value', 'buildup_score', 'virality_score']

if __name__ == "__main__":
    for i in range(len(data['jokes'])):


        data['jokes'][i]['humour_score'] = 0.0
        data['jokes'][i]['shock_value'] = 0.0
        data['jokes'][i]['buildup_score'] = 0.0
        data['jokes'][i]['virality_score'] = 0.0
    print(data)
    with open("scored_chunks.json", 'w') as file:
        json.dump(data, file, indent=2)

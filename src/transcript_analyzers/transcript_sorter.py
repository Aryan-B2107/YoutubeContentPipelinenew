import json
import os


def main():
    timestamped_path = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\transcripts\timestamped_collection.json"
    # Load scored_chunks.json
    with open(r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\data\transcripts\scored_chunks.json", "r") as f:
        scored_data = json.load(f)

    jokes = scored_data["jokes"]

    # Step 1: Compute average scores
    for joke in jokes:
        humour = joke.get("humour_score", 0.0)
        shock = joke.get("shock_value", 0.0)
        # You can include explicit content in average if needed
        average_score = (humour + shock) / 2
        joke["average_score"] = average_score

    # Step 2: Sort jokes by average score (highest to lowest)
    jokes_sorted = sorted(jokes, key=lambda j: j["average_score"], reverse=True)

    # Step 3: Extract content_ID keys in order
    sorted_content_ids = []
    for joke in jokes_sorted:
        for key in joke.keys():
            if key.lower().startswith("content_id"):
                # Capitalize 'C' in case the key starts with lowercase
                corrected_key = key[0].upper() + key[1:]
                sorted_content_ids.append(corrected_key)
                break
        else:
            print("Warning: No content_ID key found in a joke.")

    # Step 4: Load timestamped_collection.json

    with open(timestamped_path, "r") as f:
        timestamped_data = json.load(f)

    # Step 5: Reorder timestamped data
    reordered_timestamped = {}
    for cid in sorted_content_ids:
        if cid in timestamped_data:
            reordered_timestamped[cid] = timestamped_data[cid]
        else:
            print(f"Warning: {cid} not found in timestamped_collection.json")

    # Step 6: Save reordered timestamped_collection.json
    print("✅ Reordering complete based on average scores.")
    """with open(timestamped_path, "w") as f:
        json.dump(reordered_timestamped, f, indent=2)"""
    return reordered_timestamped



if __name__ == "__main__":
    main()

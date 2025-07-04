import json

def main():
    # Load scored_chunks.json
    with open("scored_chunks.json", "r") as f:
        scored_data = json.load(f)

    # Extract content_ID keys from each joke and capitalize 'c' to 'C'
    content_order = []
    for joke in scored_data["jokes"]:
        content_id_key = None
        for key in joke.keys():
            if key.lower().startswith("content_id"):
                content_id_key = key
                break
        if content_id_key:
            # Capitalize the first letter only to match timestamped keys
            corrected_key = content_id_key[0].upper() + content_id_key[1:]
            content_order.append(corrected_key)
        else:
            print("Warning: No content_ID key found in a joke.")

    # Load timestamped_collection.json (adjust your path here)
    timestamped_path = r"D:\YoutubeContentPipeline\YoutubeContentPipelineMain\src\transcribers\timestamped_collection.json"
    with open(timestamped_path, "r") as f:
        timestamped_data = json.load(f)

    # Reorder timestamped_collection.json according to content_order
    reordered_timestamped = {}
    for cid in content_order:
        if cid in timestamped_data:
            reordered_timestamped[cid] = timestamped_data[cid]
        else:
            print(f"Warning: {cid} not found in timestamped_collection.json")

    # Save reordered timestamped_collection.json back to the file
    with open(timestamped_path, "w") as f:
        json.dump(reordered_timestamped, f, indent=2)

    print("Reordering complete!")

if __name__ == "__main__":
    main()

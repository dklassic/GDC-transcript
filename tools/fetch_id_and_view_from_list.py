import requests
import csv
import re

def read_video_links(filename):
    with open(filename, "r") as file:
        video_links = file.readlines()
    return [link.strip() for link in video_links]

def extract_video_id(video_link):
    pattern = r'(?:https?:\/\/)?(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-]{11})'
    match = re.search(pattern, video_link)
    return match.group(1) if match else None

def get_video_info(video_ids, api_key):
    base_url = "https://www.googleapis.com/youtube/v3"
    endpoint = f"{base_url}/videos?id={','.join(video_ids)}&key={api_key}&part=snippet,statistics"

    response = requests.get(endpoint)
    data = response.json()

    video_data = []
    for item in data["items"]:
        video_id = item["id"]
        title = item["snippet"]["title"]
        view_count = int(item["statistics"]["viewCount"])
        video_data.append({
            "video_id": video_id,
            "title": title,
            "view_count": view_count
        })

    return video_data

def main():
    api_key = "YOUR_API_KEY"
    input_filename = "gdc_video_list.txt"

    video_links = read_video_links(input_filename)
    video_ids = [extract_video_id(link) for link in video_links if extract_video_id(link)]

    video_data = []
    # YouTube API allows a maximum of 50 video IDs per request, so split them into chunks of 50
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i + 50]
        video_data.extend(get_video_info(chunk, api_key))

    # Sort the video data by view count
    video_data.sort(key=lambda x: x["view_count"], reverse=True)

    # Create a CSV file to store the sorted data
    with open("video_data_sorted.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "video_id", "view_count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write the sorted video data to the CSV file
        for video in video_data:
            print(f"{video['title']} (ID: {video['video_id']}): {video['view_count']} views")
            writer.writerow(video)

if __name__ == "__main__":
    main()

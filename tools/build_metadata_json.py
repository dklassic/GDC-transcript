# This script is used to generate JSON files for queries on a website. 
# All generated JSONs will be placed in the './json/' directory. 
# The script will run automatically as part of the Github Action workflow.
import os
import json
from pytube import YouTube

subtitle_directory = "./static/src/subtitle"
json_directory = "./json"
subtitles_json = "./json/subtitles.json"
reviewed_subtitles_json = "./json/reviewed.json"
titles_json = "./json/titles.json"
os.makedirs(json_directory, exist_ok=True)


def getYoutubeTitle(yt : YouTube):
        # https://github.com/pytube/pytube/issues/1479
        exception_count = 0
        title = "<fetch_title_failed>"
        while (exception_count < 10):
            try:
                title = yt.title
                break
            except:
                print(f'fetch failed ({exception_count})')
                exception_count += 1
                try:
                    stream = yt.streams.first()
                except:
                    print('issues accessing stream')
                    
        return title


srt_files = [f for f in os.listdir(subtitle_directory) if f.endswith('.srt')]

srt_list = []
reviewed_list = []
titles_dict = {}

for idx, file_name in enumerate(srt_files):
    file_name_without_ext = os.path.splitext(os.path.basename(file_name))[0]
    full_file_path = os.path.join(subtitle_directory, file_name)

    videoId = file_name_without_ext
    yt = YouTube("https://www.youtube.com/watch?v=" + videoId)
    
    title = getYoutubeTitle(yt)
    yt_length = yt.length

    print(title)
    video_data = {
        "id": file_name_without_ext,
        "title": title,
        "length": yt_length,
        "subtitle": full_file_path,
        "reviewed": False,
    }
    video_json = os.path.join(json_directory, file_name_without_ext + ".json")
    with open(video_json, "w") as outfile:
        json.dump(video_data, outfile)
    print(f"Created {video_json}")
    

    srt_list.append(videoId)
    if (video_data["reviewed"]):
        reviewed_list.append(videoId)
    titles_dict[str(videoId)] = title;

with open(subtitles_json, "w") as outfile:
    json.dump(srt_list, outfile)
print(f"Created {subtitles_json}")

with open(reviewed_subtitles_json, "w") as outfile:
    json.dump(reviewed_list, outfile)
print(f"Created {reviewed_subtitles_json}")

with open(titles_json, "w") as outfile:
    json.dump(titles_dict, outfile)
print(f"Created {titles_json}")
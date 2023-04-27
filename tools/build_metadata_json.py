# This script is used to generate JSON files for queries on a website. 
# All generated JSONs will be placed in the './json/' directory. 
# The script will run automatically as part of the Github Action workflow.
import os
import json
from pytube import YouTube

subtitle_directory = "./static/src/subtitle"
metadata_directory = "./static/src/metadata"
translation_directory = "./static/src/translation"

json_directory = "./json"
subtitles_json = "./json/subtitles.json"
titles_json = "./json/titles.json"
os.makedirs(json_directory, exist_ok=True)


srt_files = [f for f in os.listdir(subtitle_directory) if f.endswith('.srt')]

srt_list = []
reviewed_list = []

video_data_dict = {}

for idx, file_name in enumerate(srt_files):
    file_name_without_ext = os.path.splitext(os.path.basename(file_name))[0]
    full_file_path = os.path.join(subtitle_directory, file_name)
    

    videoId = file_name_without_ext
    yt = YouTube("https://www.youtube.com/watch?v=" + videoId)
    
    #yt_length = yt.length

    file_metadata = os.path.join(metadata_directory, file_name_without_ext + ".meta")
    print(file_metadata)
    reviewer = ""
    explicit_permission = False
    explicit_disallowance = False
    additional_description = ""
    if (os.path.isfile(file_metadata)):
        try:
            with open(file_metadata, 'r') as file:
                srt_metadata = json.load(file)
                if 'reviewer' in srt_metadata:
                    reviewer = srt_metadata["reviewer"]
                if 'explicit_permission' in srt_metadata:
                    explicit_permission = srt_metadata["explicit_permission"]
                if 'explicit_disallowance' in srt_metadata:
                    explicit_disallowance = srt_metadata["explicit_disallowance"]
                if 'additional_description' in srt_metadata:
                    additional_description = srt_metadata["additional_description"]
        except:
            print(f"Can't load the {file_metadata} as a json file.")


    video_data = {
        "id": videoId,
        #"length": yt_length,
        "subtitle": full_file_path,
        "reviewer": reviewer,
        "explicit_permission": explicit_permission,
        "explicit_disallowance": explicit_disallowance,
        "additional_description": additional_description,
        "translation": {},
    }
    video_data_dict[str(videoId)] = video_data
    srt_list.append(videoId)

# Iterate all language directories.
subdirInTranslation = [f.path for f in os.scandir(translation_directory) if f.is_dir()]
for idx, lang_dir in enumerate(subdirInTranslation):
    lang = os.path.basename(lang_dir)
    print(lang)
    lang_subtitle_directory = os.path.join(lang_dir, "subtitle")
    if (os.path.isdir(lang_subtitle_directory)):
        # iterate .srt files in the specific langauge.
        lang_srt_files = [f for f in os.listdir(lang_subtitle_directory) if f.endswith('.srt')]
        for idx, file_name in enumerate(lang_srt_files):
            videoId = os.path.splitext(os.path.basename(file_name))[0]
            video_data_dict[str(videoId)]["translation"][str(lang)] = os.path.join(lang_subtitle_directory, file_name)

# Export jsons
for videoId, video_data in video_data_dict.items():
    video_json = os.path.join(json_directory, videoId + ".json")
    with open(video_json, "w") as outfile:
        json.dump(video_data, outfile)
    #print(f"Created {video_json}")

with open(subtitles_json, "w") as outfile:
    json.dump(srt_list, outfile)
print(f"Created {subtitles_json}")
import os
import json

subtitle_directory = "./static/src/subtitle"
output_json = "./metadata.json"

srt_files = [f for f in os.listdir(subtitle_directory) if f.endswith('.srt')]

srt_list = []

for idx, file_name in enumerate(srt_files):
    file_name_without_ext = os.path.splitext(os.path.basename(file_name))[0]
    full_file_path = os.path.join(subtitle_directory, file_name)
    srt_list.append({
        "id": file_name_without_ext,
        "subtitle": full_file_path
    })

with open(output_json, "w") as outfile:
    json.dump(srt_list, outfile)

print(f"Created {output_json}")
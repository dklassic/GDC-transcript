import argparse
import json
import os


def file_path(id, langcode):
    if(langcode == 'en'):
        file_path = f"static/src/subtitle/{id}.srt.meta"
    else:
        file_path = f'static/src/translation/{langcode}/subtitle/{id}.srt.meta'.format(langcode)
    return file_path

def main(id, langcode, jsondata):
    metadata_file_path = file_path(id, langcode)
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(metadata_file_path), exist_ok=True)
    with open(metadata_file_path, 'w') as outfile:
        json.dump(jsondata, outfile)

def json_setup(id, langcode, reviewed, reviewer,explicit_permission,explicit_disallowance,additional_description):
    if not os.path.isfile(file_path(id, langcode)):
        jsondata = {
            "reviewed": False,
            "reviewer": "",
            "explicit_permission": False,
            "explicit_disallowance": False,
            "additional_description": ""
        }
    else:
        with open(file_path(id, langcode)) as json_file:
            jsondata = json.load(json_file)
    if reviewed != "null":
        if reviewed == "true":
            jsondata["reviewed"] = True
        else:
            jsondata["reviewed"] = False
    if reviewer != "null":
        jsondata["reviewer"] = reviewer
    if explicit_permission != "null":
        if explicit_permission == "true":
            jsondata["explicit_permission"] = True
        else:
            jsondata["explicit_permission"] = False
    if explicit_disallowance != "null":
        if explicit_disallowance == "true":
            jsondata["explicit_disallowance"] = True
        else:
            jsondata["explicit_disallowance"] = False
    if additional_description != "null":
        jsondata["additional_description"] = additional_description
    return jsondata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a JSON file with reviewed flag.')
    parser.add_argument('id', type=str, help='The id of the subtitle file.')
    parser.add_argument('langcode', type=str)
    parser.add_argument('reviewed', type=str)
    parser.add_argument('reviewer', type=str)
    parser.add_argument('explicit_permission', type=str)
    parser.add_argument('explicit_disallowance', type=str)
    parser.add_argument('additional_description', type=str)
    args = parser.parse_args()
    jsondata = json_setup(args.id, args.langcode, args.reviewed, args.reviewer,args.explicit_permission,args.explicit_disallowance,args.additional_description)
    main(args.id, args.langcode, jsondata)
import sys
import json
import os


def file_path(id):
    file_path = f"static/src/metadata/{id}.meta"
    return file_path

def main(id, jsondata):
    metadata_file_path = file_path(id)
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(metadata_file_path), exist_ok=True)
    with open(metadata_file_path, 'w') as outfile:
        json.dump(jsondata, outfile)

def json_setup(id, langcode, reviewer,explicit_permission,explicit_disallowance,additional_description):
    if not os.path.isfile(file_path(id)):
        jsondata = {
            "reviewer": {},
            "explicit_permission": False,
            "explicit_disallowance": False,
            "additional_description": ""
        }
    else:
        with open(file_path(id)) as json_file:
            jsondata = json.load(json_file)
    if reviewer != "null":
        if(langcode in jsondata["reviewer"]):
            jsondata["reviewer"][langcode].append(reviewer)
        else:
            jsondata["reviewer"][langcode] = [reviewer]
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
    id = sys.argv[1]
    langcode = sys.argv[2]
    reviewer = sys.argv[3]
    explicit_permission = sys.argv[4]
    explicit_disallowance = sys.argv[5]
    additional_description = sys.argv[6]
    jsondata = json_setup(id, langcode, reviewer, explicit_permission, explicit_disallowance, additional_description)
    main(id, jsondata)
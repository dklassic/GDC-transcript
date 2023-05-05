import sys
import re
import os

def update_srt_indices(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    index = 1

    for line in lines:
        if re.match(r'^\d+$', line):
            new_lines.append(str(index))
            index += 1
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Argument mismatch.")
        sys.exit(1)

    id = sys.argv[1]
    lang_code = sys.argv[2]
    if(lang_code == 'en'):
        subtitle_base_path = 'static/src/subtitle/'
    else:
        subtitle_base_path = 'static/src/translation/{}/subtitle/'.format(lang_code)
    subtitle_filename = '{}.srt'.format(id)
    input_file = os.path.join(subtitle_base_path, subtitle_filename)
    update_srt_indices(input_file)

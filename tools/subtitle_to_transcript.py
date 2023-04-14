import sys
import os
import re

def read_subtitle_file(filepath):
    print("Reading subtitle file:", filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def write_transcript_file(filepath, transcript):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(transcript)

def convert_srt_to_transcript(srt_content):
    subtitle_lines = re.split(r'\r?\n\r?\n', srt_content)
    transcript = ''
    for line in subtitle_lines:
        if len(transcript) > 2 and transcript and transcript[-1] in '.!?':
            transcript += '\n'
        text = re.sub(r'\d+\r?\n\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\r?\n', '', line)
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'\r?\n', ' ', text).strip()
        if not text:
            continue
        if transcript and transcript[-1] not in '.!?':
            transcript += ' '
        transcript += text

    return transcript

def main(id, lang_code):
    if(lang_code == 'en'):
        subtitle_base_path = 'static/src/subtitle/'
    else:
        subtitle_base_path = 'static/src/translation/{}/subtitle/'.format(lang_code)
    subtitle_filename = '{}.srt'.format(id)
    subtitle_filepath = os.path.join(subtitle_base_path, subtitle_filename)

    if not os.path.isfile(subtitle_filepath):
        print("Subtitle file not found.")
        return

    srt_content = read_subtitle_file(subtitle_filepath)
    transcript = convert_srt_to_transcript(srt_content)

    if(lang_code == 'en'):
        transcript_base_path = 'static/src/transcript/'
    else:
        transcript_base_path = 'static/src/translation/{}/transcript'.format(lang_code)
    
    if not os.path.exists(transcript_base_path):
        os.makedirs(transcript_base_path)

    transcript_filename = '{}.txt'.format(id)
    transcript_filepath = os.path.join(transcript_base_path, transcript_filename)

    write_transcript_file(transcript_filepath, transcript)

    print("Transcript saved to:", transcript_filepath)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Argument mismatch.")
        sys.exit(1)

    id = sys.argv[1]
    lang_code = sys.argv[2]

    main(id, lang_code)
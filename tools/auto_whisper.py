import os
import sys
import json
import re
import subprocess
from pytube import YouTube
import requests

def download_video(video_id):
    video_url = 'http://youtube.com/watch?v=' + video_id
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename="video.mp3", output_path=".", skip_existing=False)

def transcribe_audio():
    headers = {
        'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}',
    }
    files = {
        'file': ('audio.wav', open('video.wav', 'rb')),
    }
    response = requests.post('https://api.openai.com/v1/whisper/asr', headers=headers, files=files)
    data = json.loads(response.text)
    return data['text']

def convert_audio_to_wav(input_file, output_file):
    subprocess.run(["ffmpeg", "-i", input_file, output_file])

def main(video_id):
    download_video(video_id)
    convert_audio_to_wav("video.mp3", "video.wav")
    transcript = transcribe_audio()

    with open(f"static/src/subtitle/{video_id}.srt", 'w', encoding='utf-8') as f:
        f.write(transcript)

if __name__ == "__main__":
    video_id = sys.argv[1]
    main(video_id)
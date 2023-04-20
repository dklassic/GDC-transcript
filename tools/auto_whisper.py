import os
import sys
import openai
from pytube import YouTube

# not sure how to do this properly yet: https://platform.openai.com/docs/guides/speech-to-text/quickstart

def download_video(video_id):
    try:
        video_url = f'http://youtube.com/watch?v={video_id}'
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(filename="video.mp3", output_path=".", skip_existing=False)
        print(f"Audio downloaded from {video_url}")
    except Exception as e:
        print(f"Error downloading audio from {video_url}: {e}")


def transcribe_audio():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    audio_file = open("video.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="srt")
    return transcript['srt']

def main(video_id):
    try:
        download_video(video_id)
        transcript = transcribe_audio()

        with open(f"static/src/subtitle/{video_id}.srt", 'w', encoding='utf-8') as f:
            f.write(transcript)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_id = sys.argv[1]
    main(video_id)
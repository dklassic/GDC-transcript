import os
from pytube import YouTube
from moviepy.editor import *
from concurrent.futures import ThreadPoolExecutor

def read_video_ids(filename):
    with open(filename, "r") as file:
        video_ids = file.readlines()
    return [video_id.strip() for video_id in video_ids]

def download_audio(video_id, output_folder):
    link = f"https://www.youtube.com/watch?v={video_id}"
    print(f"Downloading audio from {link}...")

    try:
        yt = YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_file = audio_stream.download(output_path=output_folder, filename=video_id)

        # Convert the downloaded file to MP3
        input_audio = AudioFileClip(output_file)
        input_audio.write_audiofile(os.path.join(output_folder, f"{video_id}.mp3"))
        os.remove(output_file)  # Remove the original downloaded file

        print(f"Audio downloaded from {link}")
    except Exception as e:
        print(f"Error downloading audio from {link}: {e}")

def main():
    input_filename = "video_to_download.txt"
    output_folder = "gdc_audio"

    video_ids = read_video_ids(input_filename)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Run the download process concurrently using multiple threads
    with ThreadPoolExecutor() as executor:
        executor.map(lambda video_id: download_audio(video_id, output_folder), video_ids)

if __name__ == "__main__":
    main()

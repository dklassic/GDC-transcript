import os
import subprocess

def read_video_ids(filename):
    with open(filename, "r") as file:
        video_ids = file.readlines()
    return [video_id.strip() for video_id in video_ids]

def download_audio(video_ids, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for video_id in video_ids:
        link = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Downloading audio from {link}...")
        try:
            subprocess.check_output([
                "youtube-dl",
                "-f", "bestaudio/best",
                "--extract-audio",
                "--audio-format", "mp3",
                "--output", f"{output_folder}/{video_id}.%(ext)s",
                link
            ])
            print(f"Audio downloaded from {link}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading audio from {link}: {e}")

def main():
    input_filename = "video_to_download.txt"
    output_folder = "gdc_audio"

    video_ids = read_video_ids(input_filename)
    download_audio(video_ids, output_folder)

if __name__ == "__main__":
    main()

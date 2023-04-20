import os
from pytube import YouTube
from yt_dlp import YoutubeDL
from concurrent.futures import ThreadPoolExecutor

input_filename = "video_to_download.txt"
error_output_filename = "video_download_error.txt"
output_folder = "downloaded_audio"

def read_video_ids(filename):
    with open(filename, "r") as file:
        video_ids = file.readlines()
    return [video_id.strip() for video_id in video_ids]

def add_error_video_ids(video_id):
    with open(error_output_filename, "a") as file:
        file.write(video_id + "\n")


def download_audio(video_id, output_folder):
    link = f"https://www.youtube.com/watch?v={video_id}"
    print(f"Downloading audio from {link}...")

    try:
        yt = YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_file = audio_stream.download(output_path=output_folder, filename=video_id+".mp3")
        print(f"Audio downloaded from {link}")
    except Exception as e:
        print(f"Error downloading audio from {link}: {e}. Try yt_dlp...")
        try:
            video_url = f'http://youtube.com/watch?v={video_id}'
            URLS = [video_url]
            ydl_opts = {
                "outtmpl": './' + output_folder + f'/{video_id}.%(ext)s',
                'format': 'm4a/bestaudio/best',
                # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            }

            with YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(URLS)
        except Exception as e:
            print(f"Download {link} failed: {e}. Log the error video id.")
            add_error_video_ids(link)

def main():
    video_ids = read_video_ids(input_filename)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Run the download process concurrently using multiple threads
    with ThreadPoolExecutor() as executor:
        executor.map(lambda video_id: download_audio(video_id, output_folder), video_ids)

if __name__ == "__main__":
    main()

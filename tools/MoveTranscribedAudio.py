import os
import shutil

# Set the folder paths
igds_audio_folder = "IGDS_Audio"
whisper_output_folder = "Whisper-Output"
transcribed_folder = "Transcribed"

# Check if the Transcribed folder exists, if not create it
if not os.path.exists(transcribed_folder):
    os.makedirs(transcribed_folder)

# Get the filenames from the folders
igds_audio_files = set([f[:-4] for f in os.listdir(igds_audio_folder) if f.endswith(".mp3")])
whisper_output_files = set([f[:-4] for f in os.listdir(whisper_output_folder) if f.endswith(".srt")])

# Find common filenames between the two sets
common_files = igds_audio_files.intersection(whisper_output_files)

# Move the matched mp3 files to the Transcribed folder
for file in common_files:
    src = os.path.join(igds_audio_folder, f"{file}.mp3")
    dst = os.path.join(transcribed_folder, f"{file}.mp3")
    shutil.move(src, dst)

print(f"Moved {len(common_files)} mp3 files to the Transcribed folder.")

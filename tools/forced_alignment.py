import argparse
import os
from aeneas.executetask import ExecuteTask
from aeneas.task import Task

def generate_srt(transcript_path, audio_path, output_path):
    config_string = "task_language=en|os_task_file_format=srt|is_text_type=plain"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = audio_path
    task.text_file_path_absolute = transcript_path
    task.sync_map_file_path_absolute = output_path

    ExecuteTask(task).execute()

    task.output_sync_map()

def main(id):
    transcript_path = f"{id}.txt"
    audio_path = f"{id}.mp3"
    output_path = f"{id}.srt"

    if not os.path.exists(transcript_path) or not os.path.exists(audio_path):
        print("Error: Transcript or audio file not found.")
        return

    generate_srt(transcript_path, audio_path, output_path)
    print(f"Generated SRT file: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate forced-aligned SRT subtitle using Aeneas.")
    parser.add_argument("id", help="ID of the transcript and audio files (without extension).")
    args = parser.parse_args()

    main(args.id)

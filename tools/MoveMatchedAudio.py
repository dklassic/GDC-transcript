import os
import shutil

def read_filenames(filename):
    with open(filename, "r") as file:
        filenames = file.readlines()
    return [filename.strip() for filename in filenames]

def move_files(filenames, source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for filename in filenames:
        mp3_filename = f"{filename}.mp3"
        source_path = os.path.join(source_folder, mp3_filename)
        target_path = os.path.join(target_folder, mp3_filename)

        if os.path.isfile(source_path):
            shutil.move(source_path, target_path)
            print(f"Moved {mp3_filename} to {target_folder}")
        else:
            print(f"{mp3_filename} not found in {source_folder}")

def main():
    input_filename = "to_move.txt"
    source_folder = "gdc_audio"
    target_folder = "matched_audio"

    filenames = read_filenames(input_filename)
    move_files(filenames, source_folder, target_folder)

if __name__ == "__main__":
    main()

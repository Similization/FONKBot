import os
from typing import List


def create_music_folder(path_to_music_folder: str, list_of_files: List[str]) -> None:
    os.makedirs(path_to_music_folder, exist_ok=True)
    for music_file in list_of_files:
        os.mkdir(os.path.join(path_to_music_folder, music_file))

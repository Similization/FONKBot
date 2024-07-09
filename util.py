import os
from typing import List


def create_music_folder(path_to_music_folder: str) -> None:
    os.makedirs(path_to_music_folder, exist_ok=True)

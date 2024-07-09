from dataclasses import dataclass
import os
from typing import List


class LocalMusic:
    def __init__(self, path_to_music_folder: str, path_to_ffmpeg: str) -> None:
        self._path_to_ffmpeg: str = path_to_ffmpeg
        self._path_to_music_folder: str = path_to_music_folder

        self._tracks: List[str] = os.listdir(self._path_to_music_folder)
        self._track_position: int = 0
        self._track_count: int = len(self._tracks)

    def update_music_path(self, path_to_music_folder: str):
        self._path_to_music_folder = path_to_music_folder

        self._tracks = os.listdir(self._path_to_music_folder)
        self._track_position = 0
        self._track_count = len(self._tracks)

    def update_tracks(self, path_to_music_folder: str):
        self._tracks = os.listdir(self._path_to_music_folder)
        self._track_position = 0
        self._track_count = len(self._tracks)

    def get_tracks(self) -> List[str]:
        return self._tracks

    def get_track_count(self) -> int:
        return self._track_count

    def get_track_position(self) -> int:
        return self._track_position

    def get_current_track(self) -> str:
        return self._tracks[self._track_position]

    def next_track(self, count: int = 1):
        self._track_position = (self._track_position + count) % self._track_count

    def previous_track(self, count: int = 1):
        self.track_position = (self._track_position - count) % self._track_count

import os
from typing import List
from yandex_music import ClientAsync, Playlist, Status
from yandex_music.track.track import Track as YaTrack

from config import YandexMusiclConfig
from util import create_music_folder

class AsyncYandexTrack:
    def __init__(self, track: YaTrack) -> None:
        self._name = track.title
        self._author = track.artists[0].title
        self._url = track.url
        self._duration = track.duration


class AsyncYandexMusic:
    def __init__(self, config: YandexMusiclConfig) -> None:
        self._config: YandexMusiclConfig = config
        self._client = ClientAsync(token=self._config.token)

    async def init(self) -> "AsyncYandexMusic":
        await self._client.init()
        return self

    async def search_playlist(
        self, playlist_name: str
    ) -> List[YaTrack]:

        search_result = await self._client.search(
            text=playlist_name, type_="playlist"
        )
        playlist: Playlist = search_result.playlists.results[0]
        playlist_with_tracks: Playlist = await self._client.users_playlists(kind=playlist.kind, user_id=playlist.owner.uid)
        return playlist_with_tracks
    
    async def download_playlist(
        self, playlist: Playlist
    ) -> None:
        playlist_title: str = playlist.title
        path_to_playlist_folder = os.path.join(self._config.path_to_music_folder, playlist_title)

        playlist_tracks: List[AsyncYandexTrack] = []
        for track in playlist.tracks:
            playlist_tracks.append(AsyncYandexTrack(
                track=track
            ))

        create_music_folder(path_to_music_folder=path_to_playlist_folder, list_of_files=playlist_tracks)
        return        

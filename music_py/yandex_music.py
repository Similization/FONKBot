from functools import reduce
import os
from typing import List
from yandex_music import ClientAsync, Playlist, Status
from yandex_music.track.track import Track as YaTrack
from yandex_music.album.album import Album as YaAlbum
from yandex_music.playlist.playlist import Playlist as YaPlaylist

from config import YandexMusiclConfig
from util import create_music_folder


class AsyncYandexTrack:
    def __init__(self, track: YaTrack) -> None:
        self._track: YaTrack = track
        self._name = track.title
        self._authors = ", ".join(list(map(lambda artist: artist.name, track.artists)))
        self._url = track.cover_uri
        self._duration = track.duration_ms

    def get_filename(self):
        return self._name + " - " + self._authors + ".mp3"

    async def download_track(
        self, to: str, codec: str = "mp3", bitrate_in_kbps: int = 192
    ):
        filename = os.path.join(to, self.get_filename())
        await self._track.download_async(
            filename=filename, codec=codec, bitrate_in_kbps=bitrate_in_kbps
        )


class AsyncYandexAlbum:
    def __init__(self, album: YaAlbum) -> None:
        self._album: YaAlbum = album
        self._name = album.title
        self._authors = ", ".join(list(map(lambda artist: artist.name, album.artists)))
        self._url = album.cover_uri
        self._duration = album.duration_ms
        self._tracks: List[AsyncYandexTrack] = []

    def set_album_tracks(self):
        tracks = []
        for volume in self._album.volumes:
            tracks.extend(volume)

        self._tracks = list(map(lambda track: AsyncYandexTrack(track=track), tracks))

    def get_filename(self):
        return self._name + " - " + self._authors

    async def download_album(
        self, to: str, codec: str = "mp3", bitrate_in_kbps: int = 192
    ):
        filename = os.path.join(to, self.get_filename())

        for track in self._tracks:
            await track.download_track(to=filename)


class AsyncYandexPlaylist:
    def __init__(self, playlist: YaPlaylist) -> None:
        self._playlist: YaPlaylist = playlist
        self._name = playlist.title
        self._url = playlist.cover.uri
        self._duration = playlist.duration_ms

    def get_filename(self):
        return self._name + " - " + self._authors + ".mp3"

    async def download_track(
        self, to: str, codec: str = "mp3", bitrate_in_kbps: int = 192
    ):
        filename = os.path.join(to, self.get_filename())
        await self._track.download_async(
            filename=filename, codec=codec, bitrate_in_kbps=bitrate_in_kbps
        )


class AsyncYandexMusic:
    def __init__(self, config: YandexMusiclConfig) -> None:
        self._config: YandexMusiclConfig = config
        self._client = ClientAsync(token=self._config.token)

    async def init(self) -> "AsyncYandexMusic":
        await self._client.init()
        return self

    async def search_playlist(self, playlist_name: str) -> Playlist:

        search_result = await self._client.search(text=playlist_name, type_="playlist")
        playlist: Playlist = search_result.playlists.results[0]
        playlist_with_tracks: Playlist = await self._client.users_playlists(
            kind=playlist.kind, user_id=playlist.owner.uid
        )
        return playlist_with_tracks

    async def download_playlist(self, playlist: Playlist) -> None:
        playlist_title: str = playlist.title
        path_to_playlist_folder = os.path.join(
            self._config.path_to_music_folder, playlist_title
        )
        create_music_folder(path_to_music_folder=path_to_playlist_folder)

        playlist_tracks: List[AsyncYandexTrack] = []
        for track in playlist.tracks:
            current_track = AsyncYandexTrack(track=track.track)
            playlist_tracks.append(current_track)
            await current_track.download_track(to=path_to_playlist_folder, codec="mp3")

        return

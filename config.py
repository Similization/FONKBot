from dataclasses import dataclass

import yaml


@dataclass
class DiscordConfig:
    token: str


@dataclass
class LocalMusicConfig:
    path_to_music_folder: str
    path_to_ffmpeg: str


@dataclass
class YandexMusiclConfig:
    email: str
    password: str
    token: str
    path_to_music_folder: str


@dataclass
class DiscordBotConfig:
    discord: DiscordConfig
    local_music: LocalMusicConfig
    yandex_music: YandexMusiclConfig


def config_discord() -> DiscordBotConfig:
    with open("config.yaml") as stream:
        try:
            yaml_config = yaml.safe_load(stream)
            return DiscordBotConfig(
                discord=DiscordConfig(token=yaml_config["discord"]["token"]),
                local_music=LocalMusicConfig(
                    path_to_music_folder=yaml_config["local_music"][
                        "path_to_music_folder"
                    ],
                    path_to_ffmpeg=yaml_config["local_music"]["path_to_ffmpeg"],
                ),
                yandex_music=YandexMusiclConfig(
                    email=yaml_config["yandex_music"]["email"],
                    password=yaml_config["yandex_music"]["password"],
                    token=yaml_config["yandex_music"]["token"],
                    path_to_music_folder=yaml_config["yandex_music"][
                        "path_to_music_folder"
                    ],
                ),
            )
        except yaml.YAMLError as exc:
            print(exc)

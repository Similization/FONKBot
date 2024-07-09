from dataclasses import dataclass
import os
from typing import List
from discord import Intents, VoiceClient
import nextcord
from nextcord.ext import commands

from config import DiscordBotConfig, config_discord
from music_py.music import LocalMusic
from music_py.yandex_music import AsyncYandexMusic


@dataclass
class DiscordBot(commands.Bot):
    config: DiscordBotConfig
    local_music: LocalMusic
    yandex_music: AsyncYandexMusic

    def __init__(self, config: DiscordBotConfig, intents: Intents) -> None:
        super().__init__(intents=intents)

        self.config = config
        self.local_music = LocalMusic(
            path_to_music_folder=config.local_music.path_to_music_folder,
            path_to_ffmpeg=config.local_music.path_to_ffmpeg,
        )
        self.yandex_music = AsyncYandexMusic(token=config.yandex_music.token)


config = config_discord()
intents = Intents.default()

bot = DiscordBot(config=config, intents=intents)

if not bot.config.discord.token:
    raise ValueError("TOKEN environment variable not set")
if not bot.config.local_music.path_to_music_folder:
    raise ValueError("MUSIC_PATH environment variable not set")


async def play_next(interaction: nextcord.Interaction, e: Exception = None):
    user_voice_state = interaction.user.voice
    if user_voice_state is None:
        await interaction.send("You are not in a voice channel!")
        return
    user_voice_channel = user_voice_state.channel

    voice_client: VoiceClient = None
    if len(bot.voice_clients) > 0:
        voice_client = bot.voice_clients[0]
    if voice_client is None:
        voice_client = await user_voice_channel.connect()

    current_song = bot.local_music.get_current_track()
    voice_client.play(
        source=nextcord.FFmpegOpusAudio(
            source=os.path.join(
                bot.config.local_music.path_to_music_folder, current_song
            ),
        ),
        after=lambda e=None: play_next(interaction, e),
    )

    bot.local_music.next_track(count=1)
    await interaction.send(f"Now playing {current_song}")


@bot.event
async def on_ready():
    print(f"Bot started as {bot.user}")


@bot.slash_command(description="Play FONK")
async def play(interaction: nextcord.Interaction):
    await play_next(interaction)


@bot.slash_command(description="Play next <count> FONK")
async def next(interaction: nextcord.Interaction, count: int = 1):
    if len(bot.voice_clients) > 0 and bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()

    bot.local_music.next_track(count=count - 1)
    await play_next(interaction)


@bot.slash_command(description="Play previous <count> FONK")
async def previous(interaction: nextcord.Interaction, count: int = 1):
    if len(bot.voice_clients) > 0 and bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()

    bot.local_music.previous_track(count=count + 1)
    await play_next(interaction)


@bot.slash_command(description="Stop FONK")
async def stop(interaction: nextcord.Interaction):
    user_voice_state = interaction.user.voice
    if user_voice_state is None:
        await interaction.send("You are not in a voice channel!")
        return

    if bot.voice_clients and bot.voice_clients[0].channel == user_voice_state.channel:
        await bot.voice_clients[0].disconnect()

    await interaction.send("Stopping FONK")


@bot.slash_command(description="List FONK")
async def list(interaction: nextcord.Interaction):
    user_voice_state = interaction.user.voice
    if user_voice_state is None:
        await interaction.send("You are not in a voice channel!")
        return

    if bot.voice_clients and bot.voice_clients[0].channel == user_voice_state.channel:
        await bot.voice_clients[0].disconnect()

    await interaction.send("List of FONK")


@bot.slash_command(description="List FONK")
async def yam_playlist(interaction: nextcord.Interaction, playlist_name: str):
    playlist = await bot.yandex_music.search_playlist(
        playlist_name=playlist_name, in_client=True
    )
    await interaction.send(playlist)


bot.run(bot.config.discord.token)

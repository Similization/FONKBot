import os
from typing import List
from discord import Intents, VoiceClient
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

token = os.getenv("TOKEN")
music_path = os.getenv("MUSIC_PATH")
ffmpeg_path = os.getenv("FFMPEG_PATH")

if not token:
    raise ValueError("TOKEN environment variable not set")
if not music_path:
    raise ValueError("MUSIC_PATH environment variable not set")

music_list: List[str] = os.listdir(music_path)
current_song_position: int = 0

intents = Intents.default()

bot = commands.Bot(intents=intents)

async def play_next(interaction: nextcord.Interaction, e: Exception = None):
    global current_song_position

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

    if current_song_position >= len(music_list):
        current_song_position = 0  # Loop back to the start of the playlist

    current_song = music_list[current_song_position]
    voice_client.play(
        source=nextcord.FFmpegOpusAudio(executable=ffmpeg_path, source=os.path.join(music_path, current_song)),
        after=lambda e=None: play_next(interaction, e)
    )

    current_song_position += 1

    await interaction.send(f"Now playing {current_song}")

@bot.event
async def on_ready():
    print(f'Bot started as {bot.user}')

@bot.slash_command(description="Play FONK")
async def play(interaction: nextcord.Interaction):
    await play_next(interaction)

@bot.slash_command(description="Play next <count> FONK")
async def next(interaction: nextcord.Interaction, count: int = 1):
    if len(bot.voice_clients) > 0 and bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()

    global current_song_position 
    current_song_position = (current_song_position + count - 1) % len(music_list)
    await play_next(interaction)

@bot.slash_command(description="Play previous <count> FONK")
async def previous(interaction: nextcord.Interaction, count: int = 1):
    if len(bot.voice_clients) > 0 and bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()

    global current_song_position 
    current_song_position = (current_song_position - count - 1) % len(music_list)
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

    await interaction.send("Stopping FONK")

bot.run(token)

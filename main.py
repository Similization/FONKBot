import os
from typing import List
from discord import VoiceClient
import nextcord
from nextcord.ext import commands

token = os.getenv("TOKEN")
music_path = os.getenv("MUSIC_PATH")
music_list: List[str] = os.listdir(music_path)
current_song_position: int = 0

bot = commands.Bot()

async def play_next(interaction: nextcord.Interaction, e: Exception = None):
    global current_song_position

    user_voice_state = interaction.user.voice
    if user_voice_state is None:
        await interaction.send("You are not in a voice channel!")
    user_voice_channel = user_voice_state.channel


    voice_client: VoiceClient = None
    if len(bot.voice_clients) > 0: 
        voice_client = bot.voice_clients[0]
    if voice_client is None:
        voice_client = await user_voice_channel.connect()
    

    current_song = music_list[current_song_position]
    voice_client.play(source=nextcord.FFmpegOpusAudio(f"{music_path}/{current_song}"), after=lambda e=None: play_next(interaction, e))

    current_song_position += 1

    await interaction.send(f"Now is playing {current_song}")


@bot.event
async def on_ready():
    print(f'Bot started as {bot.user}')

@bot.slash_command(description="Play FONK")
async def play(interaction: nextcord.Interaction):
    await play_next(interaction)

@bot.slash_command(description="Play next <count> FONK", )
async def next(interaction: nextcord.Interaction,  count: int = 1):
    voice_client: VoiceClient = bot.voice_clients[0]
    voice_client.stop()
    global current_song_position 
    current_song_position = (current_song_position + count) % len(music_list)
    await play_next(interaction)
        
    

@bot.slash_command(description="Play previous <count> FONK")
async def previous(interaction: nextcord.Interaction,  count: int = 1):
    voice_client: VoiceClient = bot.voice_clients[0]
    voice_client.stop()
    global current_song_position 
    current_song_position = (current_song_position - count) % len(music_list)
    await play_next(interaction)

@bot.slash_command(description="Stop FONK")
async def stop(interaction: nextcord.Interaction):
    user_voice_state = interaction.user.voice
    if user_voice_state is None:
        await interaction.send("You are not in a voice channel!")

    user_voice_channel = user_voice_state.channel
    if user_voice_channel is bot.voice_clients[0].channel:
        bot.voice_clients[0].disconnect()

    await interaction.send("Stopping FONK")

bot.run(token)

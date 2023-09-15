import discord
from discord.ext import commands
from pytube import YouTube
import yaml
import os
import asyncio  # Import the asyncio module

# Set the full path to the FFmpeg executable (replace with your path)
ffmpeg_executable = '/path/to/ffmpeg'

# Load bot settings from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Define the intents for your bot
intents = discord.Intents.all()
intents.typing = True
intents.presences = True

# Create a bot instance with intents
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

# Set the FFmpeg executable path for discord.py's FFmpegPCMAudio
discord.FFmpegPCMAudio.executable = ffmpeg_executable

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def play(ctx, url):
    # Check if the user is in a voice channel
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    # Fetch the YouTube video
    try:
        yt = YouTube(url)
    except Exception as e:
        await ctx.send(f"An error occurred while fetching the video: {e}")
        return

    # Get the best audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Check if an audio stream was found
    if audio_stream:
        # Join the user's voice channel
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        # Download and play the audio stream
        audio_stream.download()
        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(f"{yt.title}.mp4"))

        # Wait until the audio finishes playing
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Delete the downloaded mp4 file
        os.remove(f"{yt.title}.mp4")

    else:
        await ctx.send("No audio stream found for this URL.")

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await voice_client.disconnect()

# Run the bot with the token from the config.yaml file
bot.run(config['token'])
    
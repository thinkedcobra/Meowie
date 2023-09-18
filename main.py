import discord
from discord.ext import commands
from pytube import YouTube
import yaml
import os
import asyncio
from youtubesearchpython import VideosSearch
import random

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

# Initialize an empty music queue
music_queue = []

@bot.event
async def on_ready():
    print(f'>:3 {bot.user.name}')



@bot.event
async def on_message(message):
    # Avoid infinite loops by ignoring messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message content is "meow" (case-insensitive)
    if message.content.lower() == 'meow':
        return
    if message.content.startswith(config['prefix'] + 'meow'):
        random_meow = random.choice(config['speak'])
        random_emoji = random.choice(config['emoji'])
        await message.reply(str(random_meow) + '!' + str(random_emoji))

    await bot.process_commands(message)  # Important to process commands

@bot.command()
async def play(ctx, *, query):  # Accept the query as a single argument
    # Check if the user is in a voice channel
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    # Search for videos based on the query
    videos_search = VideosSearch(query, limit=1)  # Limit to 1 result

    # Get the first video from the search results
    video_url = videos_search.result()['result'][0]['link']

    # Add the video URL to the music queue
    music_queue.append(video_url)

    # If the bot is not already in a voice channel, join the user's voice channel
    if not ctx.voice_client:
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

    # Play the next song in the queue if there's one
    if not ctx.voice_client.is_playing() and music_queue:
        next_song_url = music_queue.pop(0)
        play_song(ctx.voice_client, next_song_url)

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await voice_client.disconnect()

@bot.command()
async def opgg(ctx, server_region, summoner_name):
    try:
        # Form the URL to the OP.GG page for the summoner
        opgg_url = f"https://{server_region.lower()}.op.gg/summoner/userName={summoner_name.replace(' ', '+')}"

        # Send the URL as a message in the Discord channel
        await ctx.send(f"OP.GG Stats for {summoner_name} on {server_region}: {opgg_url}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def queue(ctx, *, query):  # Accept the query as a single argument
    # Search for videos based on the query
    videos_search = VideosSearch(query, limit=1)  # Limit to 1 result

    # Get the first video from the search results
    video_url = videos_search.result()['result'][0]['link']

    # Add the video URL to the music queue
    music_queue.append(video_url)

    await ctx.send(f"Added '{videos_search.result()['result'][0]['title']}' to the queue.")

@bot.command()
async def skip(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Skipped the current song.")

def play_song(voice_client, song_url):
    yt = YouTube(song_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    # Download and play the audio stream
    audio_stream.download() 
    voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(f"{yt.title}.mp4"))
    
    # Wait until the audio finishes playing
    while voice_client.is_playing():
        asyncio.sleep(1)
    
    # Delete the downloaded mp4 file
    os.remove(f"{yt.title}.mp4")

# Run the bot with the token from the config.yaml file
bot.run(config['token'])

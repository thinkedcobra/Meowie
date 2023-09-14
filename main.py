import discord
from discord.ext import commands
import youtube_dl
import yaml

# Load bot settings from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Define the intents for your bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Create a bot instance with intents
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(url2))

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await voice_client.disconnect()

# Run the bot with the token from the config.yaml file
bot.run(config['token'])

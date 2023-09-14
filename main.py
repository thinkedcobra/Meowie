import discord
import yaml
import random


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'>:3 {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(config['prefix'] + 'meow'):
        random_meow = random.choice(config['speak'])
        random_emoji = random.choice(config['emoji'])
        await message.reply(str(random_meow) + '!' + str(random_emoji))



client.run(config['token'])

# imporing libaries
import discord
import yaml
import random

# loading config file
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


# allowing intents
intents = discord.Intents.default()
intents.message_content = True
# creating new client 
client = discord.Client(intents=intents)
# sending print to cmd when bot start
@client.event
async def on_ready():
    print(f'>:3 {client.user}')
# 1st command
@client.event
async def on_message(message):
    # randomimzing the "meow" and "emoji" used then sending msg
    if message.author == client.user:
        return
    if message.content.startswith(config['prefix'] + 'meow'):
        random_meow = random.choice(config['speak'])
        random_emoji = random.choice(config['emoji'])
        await message.reply(str(random_meow) + '!' + str(random_emoji))


# running client
client.run(config['token'])

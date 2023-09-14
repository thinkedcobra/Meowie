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


    if message.content.startswith('meow'):
        await message.reply('Meow! <a:meowieCatKiss:1151597399807111288>')

    if message.content.startswith('?h'):
        await message.reply('M-meow. How can i help? If you need toknow a command type "COMMANDS".')

    if message.content.startswith('COMMANDS'):
        await message.reply('?p- Play something ?h- Help ?smurf- Smurf cat')

    if message.content.startswith('?p'):
        await message.reply('What would you like to play')
        
    if message.content.startswith('taylor swift'):
        await message.reply('NO FUCK YOU')

    if message.content.startswith('?smurf'):
        await message.reply('https://tenor.com/view/realistic-cat-smurf-meme-funny-gif-5895795080802392404')


client.run(config['token'])

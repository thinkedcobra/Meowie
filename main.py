import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$meow'):
        await message.channel.send('Meow!')

client.run('MTE1MTQ4MzkyMDIzMjIyNjg5Nw.GiXnhs.o-KqiNvx8B7LusKDOAqj8ES8yfGBtIcNfHSqns')

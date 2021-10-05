import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import music
import general

load_dotenv()

apiKey = os.getenv("discord-api-key")
client = commands.Bot(command_prefix='?', intents = discord.Intents.all())

cogs = [music, general]

for cog in cogs:
    cog.setup(client)

@client.event
async def on_ready():
    print(f'{client.user} well hi!')
    print(f'Server population: {len([member.name for member in client.guilds[0].members])}')

client.run(apiKey)
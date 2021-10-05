import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import music

load_dotenv()

apiKey = os.getenv("discord-api-key")
client = commands.Bot(command_prefix='?', intents = discord.Intents.all())

cogs = [music]

for cog in cogs:
    cog.setup(client)

client.run(apiKey)
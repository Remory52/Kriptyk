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
    print(f'{client.user.name} is running!')
    #print(f'Server population: {len([member.name for member in client.guilds[0].members])}')

@client.event
async def process_commands(msg):
    ctx = await client.get_context(msg, cls=commands.Context)

    if ctx.command is not None:
        await client.invoke(ctx)
    else:
        #await msg.reply("Can't wait!")
        pass

@client.event
async def on_message(msg):
    if not msg.author.bot:
        await client.process_commands(msg)

client.run(apiKey)
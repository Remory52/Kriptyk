import sys
import discord
from discord.ext import commands
import music

class general(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "kill", aliases=["shutdown", "sh"])
    async def kill(self, ctx):
        if ctx.author.name == "Remory":
            try: 
                await ctx.voice_client.disconnect()
            except:
                pass
            await ctx.send("Pulling the cord.")
            sys.exit()
        await ctx.send("You are not authorized to execute this command!")

    @commands.command(name = "whoami")
    async def whoami(self, ctx):
        roles = [name[name.find("name=") + 5:-1] for name in str(ctx.author.roles)[0:-1].replace("'", "").split(',')]
        await ctx.send(str(ctx.author.name) + " Roles:" + str(roles))

    @commands.command(name = "list")
    async def list(self, ctx):
        pass

def setup(client):
    client.add_cog(general(client))
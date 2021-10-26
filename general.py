import os
import sys
import discord
from discord.ext import commands
import urllib.request
import ssl

class general(commands.Cog):    
    def __init__(self, client):
        self.client = client

    @commands.command(name = "ip", aliases=["get_ip"], help="Get the Server's IP Address.")
    async def ip(self, ctx):
        if str(ctx.author) == str(os.getenv("owner")):
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context
            await ctx.send("Server's IP address is: " + urllib.request.urlopen('https://ident.me').read().decode('utf8'))
        else:
            await ctx.send("You are not authorized to execute this command!")

    @commands.command(name = "kill", aliases=["shutdown", "sh"], help="Shutdown Kriptyk.")
    async def kill(self, ctx):
        if str(ctx.author) == str(os.getenv("owner")):
            try: 
                await ctx.voice_client.disconnect()
            except:
                pass
            await ctx.send("Pulling the cord.")
            sys.exit()
        await ctx.send("You are not authorized to execute this command!")

    @commands.command(name = "whoami", help="Fetch your username and role(s) on the server.")
    async def whoami(self, ctx):
        roles = [f"`{role.name}`" for role in ctx.author.roles]
        await ctx.send(f"User: {str(ctx.author.name)} \nRoles: \n" + "\n".join(roles))

    @commands.command(name = "whois", help="Fetch someones role(s) on the server by their username.")
    async def whois(self, ctx):
        pass

    @commands.command(name = "list")
    async def list(self, ctx):
        pass

    @commands.command(name = "say", help="Make the bot say whatever you want it to say.")
    async def say(self, ctx, *args):
        msg = ' '.join(args)
        if msg[0] != '?':
            await ctx.message.delete()
            await ctx.send(msg)
        else:
            await ctx.send(file=discord.File("gifs/nice_try.gif"))

def setup(client):
    client.add_cog(general(client))
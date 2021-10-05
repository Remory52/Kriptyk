import youtube_dl
import discord
from discord.ext import commands

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "join", aliases=["come"])
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("dik cigaany")
        
        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_channel.move_to(voice_channel)

    @commands.command(name = "disconnect", aliases=["leave"])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name = "play", aliases=["start"])
    async def play(self, ctx, url):
        try:
            ctx.voice_client.stop()
        except:
            pass
        
        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
        YDL_OPTIONS = {'format':'bestaudio'}

        voice_client = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS) 
            voice_client.play(source)

    @commands.command(name = "pause", aliases=["hold"])
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command(name = "resume")
    async def resume(self, ctx):
        ctx.voice_client.resume()

    @commands.command(name = "stop", aliases=["cut"])
    async def stop(self, ctx):
        ctx.voice_client.stop()


def setup(client):
    client.add_cog(music(client))


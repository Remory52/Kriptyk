import youtube_dl
import discord
from discord.ext import commands
#import searchEngine
import time

class queue:
    def __init__(self):
        self.queue = []

    def nextSong(self):
        song = self.queue.pop(0)

        return song

    def addSong(self, url):
        self.queue.append(url)

    def clear(self):
        self.queue.clear()

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.que = queue()

    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
    YDL_OPTIONS = {'format':'bestaudio', 'quiet':True}

    @commands.command(name = "join", aliases=["j", "connect", "c"])
    async def join(self, ctx, *args):
        channel = None
        if args != tuple():
            channel = discord.utils.find(lambda c: str(c.name) == ' '.join(args), ctx.guild.voice_channels)
        else:
            if ctx.author.voice == None:
                await ctx.send("Connect to a channel first please.")
                return

            channel = ctx.author.voice.channel

        if channel is None and args != tuple():
            await ctx.send("A channel with this name does not exist.")
            return

        if len(ctx.bot.voice_clients) == 0:
            await channel.connect()
        else:
            if ctx.bot.voice_clients[0].channel.name == channel.name:
                return
            else:
                await ctx.voice_client.disconnect()
                time.sleep(0.5)
                await channel.connect()

        ctx.voice_client.stop()

    @commands.command(name = "disconnect", aliases=["leave", "l"])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name = "play", aliases=["start"])
    async def play(self, ctx, url):
        if url != "SKIP":
            await music.join(self, ctx)
        
        voice_client = ctx.voice_client

        if(len(self.que.queue) == 0):
            self.que.addSong(url)
            #if searchEngine.searchEngine.isUrl(url):
            #    self.que.addSong(url)
            #else:
            #    song = searchEngine.searchEngine.makeQuery(url)
            #    self.que.addSong(song)

        ctx.voice_client.stop()

        await ctx.message.delete()

        info = youtube_dl.YoutubeDL(music.YDL_OPTIONS).extract_info(self.que.nextSong(), download=False)
        await ctx.send(f"**Playing:** `{info['title']}`")
        streamingURL = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(streamingURL, **music.FFMPEG_OPTIONS) 
        voice_client.play(source)

    @commands.command(name = "skip", aliases=["sk", "s"])
    async def skip(self, ctx):
        if 0 < len(self.que.queue):
            ctx.voice_client.stop()
            await music.play(self, ctx, "SKIP")
        else:
            await ctx.message.delete()
            await ctx.send(f"The queue is empty {ctx.author.name}!")

    @commands.command(name = "queue", aliases=["que"])
    async def queue(self, ctx, url):
        await ctx.message.delete()
        title = youtube_dl.YoutubeDL(music.YDL_OPTIONS).extract_info(url, download=False)['title']
        await ctx.send(f"**Queued:** `{title}`")
        self.que.addSong(url)

    @commands.command(name = "clear", aliases=["clearq", "cq"])
    async def clear_queue(self, ctx):
        self.que.clear()

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


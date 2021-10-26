import youtube_dl
import discord
from discord.ext import commands
import searchEngine
import time

class queue:
    def __init__(self):
        self.queue = []

    def nextSong(self):
        song = self.queue.pop(0)

        return song

    def addSong(self, song):
        self.queue.append(song)

    def clear(self):
        self.queue.clear()

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.que = queue()

    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
    YDL_OPTIONS = {'format':'bestaudio', 'quiet':True}

    @commands.command(name = "join", aliases=["j", "connect", "c"], help="Join a given voice chat.")
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

    @commands.command(name = "disconnect", aliases=["leave", "l"], help="Leave voice chat.")
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name = "play", aliases=["start"], help="Play a given media.")
    async def play(self, ctx, *args):
        url = ' '.join(args)

        if url != "SKIP":
            await music.join(self, ctx)
        
        voice_client = ctx.voice_client
        await ctx.message.delete()

        progress = await ctx.send("Searching... :satellite:")

        if(len(self.que.queue) == 0):
            if searchEngine.searchEngine.isUrl(url):
                info = youtube_dl.YoutubeDL(music.YDL_OPTIONS).extract_info(url, download=False)
                self.que.addSong((info['title'], info['formats'][0]['url']))
            else:
                song = searchEngine.searchEngine.search(url)
                self.que.addSong(song)
            

        ctx.voice_client.stop()
        nextSong = self.que.nextSong()

        await progress.delete()
        await ctx.send(f"**Playing:** `{nextSong[0]}`")
        source = await discord.FFmpegOpusAudio.from_probe(nextSong[1], **music.FFMPEG_OPTIONS) 
        voice_client.play(source)

    @commands.command(name = "skip", aliases=["sk", "s"], help="Skip the now playing media.")
    async def skip(self, ctx):
        if 0 < len(self.que.queue):
            ctx.voice_client.stop()
            await music.play(self, ctx, "SKIP")
        else:
            await ctx.message.delete()
            await ctx.send(f"The queue is empty {ctx.author.name}!")

    @commands.command(name = "queue", aliases=["que"], help="Queue a song or a sound effect for future playing.")
    async def queue(self, ctx, *args):
        await ctx.message.delete()

        url = ' '.join(args)
        if searchEngine.searchEngine.isUrl(url):
            info = youtube_dl.YoutubeDL(music.YDL_OPTIONS).extract_info(url, download=False)
            self.que.addSong((info['title'], info['formats'][0]['url']))
            await ctx.send(f"**Queued:** `{info['title']}`")
        else:
            song = searchEngine.searchEngine.search(url)
            self.que.addSong(song)
            await ctx.send(f"**Queued:** `{song[0]}`")

    @commands.command(name = "clear", aliases=["clearq", "cq"], help="Clear the media queue.")
    async def clear_queue(self, ctx):
        self.que.clear()

    @commands.command(name = "pause", aliases=["hold"], help="Pause playing media.")
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command(name = "resume", aliases=["res"], help="Resume playing media.")
    async def resume(self, ctx):
        ctx.voice_client.resume()

    @commands.command(name = "stop", aliases=["cut"], help="Stop playing media.")
    async def stop(self, ctx):
        ctx.voice_client.stop()


def setup(client):
    client.add_cog(music(client))


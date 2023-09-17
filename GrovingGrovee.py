import discord
from discord.ext import commands
import youtube_dl

# Initialize the bot
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, url):
    ydl_opts = {'format': 'bestaudio/best'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client = ctx.voice_client

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn',
        }

        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url2, **FFMPEG_OPTIONS))

@bot.command()
async def pause(ctx):
    ctx.voice_client.pause()

@bot.command()
async def resume(ctx):
    ctx.voice_client.resume()

@bot.command()
async def stop(ctx):
    ctx.voice_client.stop()

# Run the bot
bot.run('BOT_TOKEN')

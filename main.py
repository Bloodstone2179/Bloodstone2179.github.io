import discord
from discord.ext import commands, tasks
import youtube_dl
import os
import asyncio
import yt_dlp

client = commands.Bot(command_prefix="!")


#keeps it up
@client.event
async def on_ready():
  change_status.start()
  print("Your bot is ready")

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next("Playing banging music RN")))



@client.command()
async def helper(ctx):
    await ctx.send("""_______ HELP _______\n 
              - !join - joins your current voice channel 
              - !play [youtube url]  - plays the song from the yt url\n 
              - !leave - the bot leaves the vc           
              - !resume resumes the pasued song\n
              - !pause pauses the song playing           
              - !stop stops the song all together cant unpause\n
              - !helper displays this help box

    """)


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  
    if voice is None or not voice.is_connected():
      await channel.connect()
      voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
@client.command()
async def play(ctx, url : str):
    if url == None:
        ctx.send("Please i9nclude a youtubr url. please refer to !helper to see how to")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '2000',
        }],
    }
    channel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
            if voice is None or not voice.is_connected():
                await channel.connect()
                voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("song.mp3")))
    voice.source.volume = 0.25

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run('OTQzODg1NjYxNzA0OTUzODY2.Yg5kBg.O9rjj__VZElYW7Vh4V95oTZpx58')

import discord
import requests
import json
import os
from keep_alive import keep_alive
from discord.ext import commands
import random
import youtube_dl
from requests import get
import json
import asyncio
from discord.ext import tasks

# cogs = [music]
#client = discord.Client()
from datetime import datetime

client = commands.Bot(command_prefix='!')

morning_time = '01:30'
test_time = '16:49'
print(datetime.strftime(datetime.now(),'%H:%M'))

sad_words = ["sad", "depressed", "unhappy", "angry", "nervous", "depressing"]
bad_words = [
    "fuck", "suck", "sucker", "fucker", "fucking", "shit", "diu", "shit",
    "wtf", "wth"
]

channel = client.get_channel(YOUR_CHANNEL)

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n -" + json_data[0]['a']
    return quote


def guess():
    num = random.random()
    if num >= 0 and num <= 0.25:
        return 'A'
    elif num > 0.25 and num <= 0.5:
        return 'B'
    elif num > 0.5 and num <= 0.75:
        return 'C'
    else:
        return 'D'


def guessSpec(num):
    num = int(num)
    rand = random.random()
    length = 1 / num
    final = 0
    i = 0
    while i <= 1:
        if rand <= i:
            break
        i = i + length
        final = final + 1
    print(rand)
    if final:
        return str(final)
    else:
        return "ErrorInput"


def user_name(name):
    final = ''
    for i in name:
        if i == '#':
            break
        final = final + i
    return final


@client.event
async def on_ready():
    print("hi fxxkers, I'm {0.user}".format(client))


@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    if message.content.startswith("lol"):
        await message.channel.send("Stop laughing, idiot")
    if message.content.startswith("i love"):
        await message.channel.send("i love you too.")
    if message.content.startswith("hello") or message.content.startswith("hi"):
        await message.channel.send('Hi, ' +
                                   user_name(str(message.author)))
    if message.content.startswith("jiayao"):
        await message.channel.send("jiayao is not here, don't disturb him")
    if message.content.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)
    if any(word in msg for word in sad_words):
        quote = get_quote()
        await message.channel.send("It's ok!!\n" + quote)
    if message.content.startswith("bye"):
        await message.channel.send("bye")
    if message.content == "GodBlessMe":
        await message.channel.send("Answer: " + guess())
    elif message.content.startswith("GodBlessMe"):
        await message.channel.send("Answer: " +
                                   guessSpec(message.content[10:]))
    if any(word in msg for word in bad_words):
        await message.channel.send("No bad words!!")
    if message.content.startswith("meme") or message.content.startswith(
            "Meme"):
        await message.channel.send("Meme time!!")
    await client.process_commands(message)


@client.command()
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content, )
    meme = discord.Embed(
        title=f"{data['title']}",
        Color=discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.reply(embed=meme)


@client.command()
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send(
            "Wait for the current playing music to end or use the 'stop' command"
        )
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format':
        'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception:
            await ctx.send("Invalid urls")
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


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


keep_alive()
client.run(os.environ['TOKEN1'])
     

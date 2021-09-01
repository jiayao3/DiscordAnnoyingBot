import discord
import requests
import json

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "nervous", "depressing"]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data  = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


@client.event
async def on_ready():
    print("hi fxxkers, I'm {0.user}".format(client));

@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    if message.content.startswith("hello") or message.content.startswith("hi"):
        await message.channel.send('Hi, fuxker')
    if message.content.startswith("jiayao"):
        await message.channel.send("jiayao is not here, don't disturb him")
    if message.content.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)
    if any(word in msg for word in sad_words):
        quote = get_quote()
        await message.channel.send("It's ok!!\n" + quote)

    

client.run('ODgyNTcxMDYzMjk1MzQ0NjYw.YS9UWg.Y8l6sd08l0twl41kGPnxX05J3jE')
     
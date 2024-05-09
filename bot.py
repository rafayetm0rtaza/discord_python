import discord
import os
import random
import requests
import json
import http.client
import math

# Import Intents
from discord import Intents

# Define the intents needed
intents = Intents.default()
intents.messages = True

# Create the client object with the necessary intents
client = discord.Client(intents=intents)


def get_hadith():
    conn = http.client.HTTPSConnection("api.sunnah.com")
    payload = "{}"
    headers = {'x-api-key': "Put your API KEY HERE "}  # Use https://alquran.cloud/api for all the API KEYS
    conn.request("GET", "/v1/hadiths/random", payload, headers)
    response = conn.getresponse()
    data = response.read()
    x = data.decode("utf-8")
    y = x[:x.find("<br")]
    a = y[y.find(">"):]  # line 28 and 29 are to get rid of the <br> and the text before it

    return a


def get_ayah():
    n = random.randint(0, 6236)
    h = str(n)
    r = requests.get("http://api.alquran.cloud/v1/ayah/" + h + "/en.asad")
    f = r.text
    q = f[f.find("text"):f.find("edition")]
    return q


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    if message.content.startswith('$hadith'):
        hadith = get_hadith()
        await message.channel.send(hadith)
    if message.content.startswith('$ayah'):
        ayat = get_ayah()
        await message.channel.send(ayat)
    if message.content.startswith('$help'):
        await message.channel.send('Commands: $hadith, $ayah')


client.run(os.getenv(
    'token'))  # create a .env file and store your token in that file. Use the token taken from discord dev portal.

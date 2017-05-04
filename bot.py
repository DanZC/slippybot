import discord
import asyncio

client = discord.Client()

@client.event
@async.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
@async.coroutine
def on_message(message):
    if message.content.startswith('!ping'):
        client.send_message(message.channel, "Pong!")
    elif message.content.startswith('!help'):
        client.send_message(message.channel, "Commands: \n !ping - Pong!")

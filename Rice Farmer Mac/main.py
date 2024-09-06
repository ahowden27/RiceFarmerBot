from creds import bot_token
import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio

client = commands.Bot(command_prefix='-', intents=discord.Intents.all())

bot_status = cycle(['Rice Farming Simulator'])

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    await client.tree.sync()
    print("Awaiting rice to be farmed.")
    change_status.start()

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with client:
        await load()
        await client.start(bot_token)

asyncio.run(main())
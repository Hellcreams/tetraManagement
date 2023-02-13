import random
import json
import asyncio
import os
from tetraBot.util import util

import discord
from discord.ext import commands, tasks
import aioconsole

intents = discord.Intents().all()

client = commands.Bot(intents=intents, command_prefix='=!', help_command=None)

file_name = "token.man"
with open(file_name, 'r', encoding="utf-8") as file:
    TOKEN = file.read()

# console command
"""
@tasks.loop(seconds=1)
async def send_console_msg():
    cc = await aioconsole.ainput()
    await client.get_channel(1019905130956607551).send(cc)
"""


@client.event
async def on_ready():
    cogs_path = os.getcwd() + "/cogs"
    cogs = os.listdir(cogs_path)
    print(cogs)
    print(cogs[0][-3:])

    for cog in cogs:
        if cog[-3:] == ".py":
            await client.load_extension(cog)

    await client.load_extension('cogs.addon')

    await client.change_presence(status=discord.Status.online, activity=discord.Game("@_@"))
    print("Bot is ready.")


client.run(TOKEN)
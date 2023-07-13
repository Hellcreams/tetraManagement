import random
import json
import asyncio
import sys
from tetraBot.util import util

import discord
from discord.ext import commands, tasks
import aioconsole

intents = discord.Intents().all()

client = commands.Bot(intents=intents, help_command=None)
test_mode = "-t" in sys.argv

file_name = "sources/source.json" \
    if test_mode else "sources/source_real.json"
with open(file_name, 'r', encoding="utf-8") as file:
    sources = json.load(file)

file_name = "token.man"
with open(file_name, 'r', encoding="utf-8") as file:
    TOKEN = file.read()

# console command

@tasks.loop(seconds=1)
async def send_console_msg():
    cc = await aioconsole.ainput()
    await client.get_channel(1019905130956607551).send(cc)


@client.event
async def on_ready():
    await client.load_extension('cogs.addon')

    if test_mode:
        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("점검 중이에요!"))
        print("Bot is ready for development.")
    else:
        await client.change_presence(status=discord.Status.online, activity=discord.Game("@_@"))
        print("Bot is ready for service.")


client.run(TOKEN)
import discord
from discord import ui
from discord.ext import commands, tasks
import os
import sys

intents = discord.Intents().all()
client = commands.Bot(intents=intents, command_prefix="*!", help_command=None)

# Read Token
file_name = "token.man"
with open(file_name, 'r', encoding="utf-8") as file:
    TOKEN = file.read()


@client.event
async def on_ready():
    cogs_ready, cogs_not_ready = 0, 0
    # load cogs
    os.chdir("cogs")
    for f in os.listdir("."):
        if f.endswith(".py"):
            try:
                await client.load_extension("cogs." + f.replace(".py", ""))
                cogs_ready += 1
            except Exception as e:
                print(f"Cog {f} has not loaded: {e}", file=sys.stderr)
                cogs_not_ready += 1
    os.chdir("..")
    print(f"Loading Cogs : Success({cogs_ready}), Failure({cogs_not_ready})")

    # done
    print("Bot Online.")


@client.tree.command(name="what", description="testing")
async def what(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


client.run(TOKEN)

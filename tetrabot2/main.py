import discord
from discord import ui
from discord.ext import commands, tasks

intents = discord.Intents().all()
client = commands.Bot(intents=intents, command_prefix="*!", help_command=None)

# Read Token
file_name = "token.man"
with open(file_name, 'r', encoding="utf-8") as file:
    TOKEN = file.read()


@client.event
async def on_ready():
    try:
        await client.load_extension('cogs.register')
    except discord.ext.commands.errors.ExtensionError:
        print("No Extension.")

    print("Bot Online.")


@client.tree.command(name="what", description="testing")
async def what(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


client.run(TOKEN)

import discord
from discord.ext import commands
import tetraBot.util


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")


def setup(client):
    return client.add_cog(Example(client))
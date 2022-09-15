from discord.ext import commands
from tetraBot.cog_util import *
import random


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {self.client.latency:.3f}s")

    @commands.command(aliases=["도움말"])
    async def help(self, ctx):
        with open("help_command.txt", "r", encoding="utf-8") as text:
            await ctx.author.send(text.read())
        return

    @commands.command(aliases=["굴려"])
    async def roll(self, ctx):
        args = get_args(ctx.message)

        if len(args) < 2:
            await ctx.send("굴릴 대상을 적어주세요. `주사위`, `동전`, `발로란트맵` 등")
            return

        if args[1] == "주사위":
            await ctx.message.reply(f"주사위 굴려욧! : `{random.randint(1, 6)}`")
            return

        if args[1] == "동전":
            await ctx.message.reply(f"동전 굴려욧! : `{random.choice(['앞', '뒤'])}`")
            return

        if args[1] == "발로란트맵":
            await ctx.message.reply(f"맵을 골라버려욧! : `{random.choice(sources['vlrt_maps'])}`")
            return


def setup(client):
    return client.add_cog(Example(client))

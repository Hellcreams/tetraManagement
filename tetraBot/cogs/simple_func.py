from discord.ext import commands
from tetraBot.util import util
import random


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.sources = util.get_source()

    def has_role(self, member, role_name):
        return self.client.get_guild(
            self.sources["guild_id"]).get_role(self.sources["role_id"][role_name]) in member.roles

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {self.client.latency:.3f}s")

    @commands.command(aliases=["도움말"])
    async def help(self, ctx):
        with open("../util/help_command.txt", "r", encoding="utf-8") as text:
            await ctx.author.send(text.read())
        return

    @commands.command(aliases=["굴려"])
    async def roll(self, ctx):
        args = util.get_args(ctx.message)

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
            await ctx.message.reply(f"맵을 골라버려욧! : `{random.choice(self.sources['vlrt_maps'])}`")
            return


def setup(client):
    return client.add_cog(Example(client))

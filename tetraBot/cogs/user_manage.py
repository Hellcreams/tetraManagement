from discord.ext import commands, tasks
from tetraBot.util import util
import asyncio


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.role_list = util.get_source("role_id")
        self.guild_id = util.get_source("guild_id")

    def has_role(self, member, role_name):
        return self.client.get_guild(self.guild_id).get_role(self.role_list[role_name]) in member.roles

    @tasks.loop(hours=23)
    async def remove_guest(self, automatic=True):
        if automatic:
            await asyncio.sleep(util.seconds_until(10, 00))
        print("Guest kick activated. auto=", automatic, sep="")
        for member in self.client.get_guild(self.guild_id).members:
            if Example.has_role(member, "GUEST"):
                await member.kick()


def setup(client):
    return client.add_cog(Example(client))


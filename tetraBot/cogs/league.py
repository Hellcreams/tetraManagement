import discord
from discord.ext import commands
from tetraBot.util import util
import asyncio
import random


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.sources = util.get_args()

    def has_role(self, member, role_name):
        return self.client.get_guild(
            self.sources["guild_id"]).get_role(self.sources["role_id"][role_name]) in member.roles

    @commands.command(aliases=["리그모집"])
    async def set_league_options(self, ctx):
        if not ctx.guild:
            return

        args = util.get_args(ctx.message)
        embed_recruit = discord.Embed(
            title="리그 모집",
            description=' '.join(args[1:]),
            colour=discord.colour.Color(0xFFFFFF)
        )
        embed_recruit.set_footer(text=f"recruited by {ctx.author.display_name}", icon_url=ctx.author.display_avatar)
        embed_recruit.add_field(name="인원", value=f"0/10")

        msg = await ctx.send(f"""<@&{self.sources['role_id']['TETRA']}>
            <@&{self.sources['role_id']['TEST']}>""", embed=embed_recruit)
        await msg.add_reaction(self.sources["emoji"]["리그"])
        # await msg.add_reaction("❌")

        try:
            while True:
                payload = await self.client.wait_for(
                    'raw_reaction_add', timeout=6.0 * 3600, check=lambda pay: pay.message_id == msg.id)

                # load raw reaction
                ch = self.client.get_channel(payload.channel_id)
                msg = await ch.fetch_message(payload.message_id)
                raw_reaction = discord.utils.get(msg.reactions, emoji=payload.emoji)

                if raw_reaction is not None:
                    if raw_reaction.emoji.id == 980433210628505670:
                        embed_recruit.set_field_at(index=0, name="인원", value=f"{raw_reaction.count - 1}/10")
                        await msg.edit(embed=embed_recruit)
                        if raw_reaction.count > 2:
                            break
                else:
                    if payload.emoji.name == "❌":
                        raise asyncio.TimeoutError

        except asyncio.TimeoutError:
            await msg.clear_reactions()
            embed_recruit.title += " (취소)"
            embed_recruit.colour = 0xFF0000
            await msg.edit(embed=embed_recruit)
            return

        user_list = []

        async for member in raw_reaction.users():
            if not member.bot:
                user_list.append("`" + member.display_name + "`")
        chief_list = random.sample(user_list, k=2)

        embed_result = discord.Embed(
            title="리그 모집 완료",
            description=f"**{chief_list[0]}, {chief_list[1]} 님**이 **팀장**입니다!",
            colour=discord.colour.Color(0x00FF00)
        )

        embed_result.set_image(
            url="https://cdn.discordapp.com/attachments/904390084491624479/991611060907933696/1-5.gif")
        embed_result.add_field(name="선공", value=f"{random.choice(chief_list)}", inline=True)
        embed_result.add_field(name="선픽", value=f"{random.choice(chief_list)}", inline=True)
        embed_result.add_field(name="전장", value=random.choice(self.sources["vlrt_maps"]), inline=True)
        embed_result.add_field(name="참여자", value=" ".join(user_list), inline=False)
        msg = await ctx.send(embed=embed_result)

        await msg.add_reaction("🏁")
        await msg.add_reaction("🗺️")

        if len(user_list) != 10:
            await msg.reply(f":bangbang: 주의 :bangbang:\n 현재 인원 수가 "
                            f"{len(user_list)}명인 것으로 확인되었습니다! 인원 재확인/조정 후 리그를 진행해주세요.")

        try:
            while True:
                reaction, member = await self.client.wait_for('reaction_add', timeout=1.0 * 3600,
                                                         check=lambda react, _: react.message.id == msg.id)

                await reaction.remove(member)

                if member != ctx.author and not Example.has_role(member, "ADMIN"):
                    await member.send("권한이 부족합니다.\n관리자 또는 리그를 소집한 분만 팀장/맵을 변경할 수 있습니다.")
                    continue

                if reaction.emoji == "🏁":
                    chief_list = random.sample(user_list, k=2)
                    embed_result.description = f"**{chief_list[0]}, {chief_list[1]}** 님이 **팀장**입니다!"
                    embed_result.set_field_at(0, name="선공", value=f"{random.choice(chief_list)}", inline=True)
                    embed_result.set_field_at(1, name="선픽", value=f"{random.choice(chief_list)}", inline=True)
                    await msg.edit(embed=embed_result)

                elif reaction.emoji == "🗺️":
                    embed_result.set_field_at(2, name="전장", value=random.choice(self.sources["vlrt_maps"]), inline=True)
                    await msg.edit(embed=embed_result)

        except asyncio.TimeoutError:
            await msg.clear_reactions()


def setup(client):
    return client.add_cog(Example(client))

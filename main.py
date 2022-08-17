import discord
from discord.ext import commands, tasks
from util import *
import random
import json
import asyncio
import aioconsole

intents = discord.Intents().all()

client = commands.Bot(intents=intents, command_prefix='=!', help_command=None)

file_name = "source_test.json"    # 소스 파일 (normal, test)
with open(file_name, 'r', encoding="utf-8") as file:
    sources = json.load(file)


def is_from_guild(ctx):
    if isinstance(ctx.author, discord.Member):
        return True
    else:
        return False


def has_role(member, role_name):
    return client.get_guild(sources["guild_id"]).get_role(role_id=sources["role_id"][role_name]) in member.roles


@tasks.loop(hours=24)
async def job_guest(automatic=True):
    lprint("Guest kick activated. auto=", automatic, sep="")
    if automatic:
        await asyncio.sleep(seconds_until(10, 00))
    for member in client.get_guild(sources["guild_id"]).members:
        if has_role(member, "GUEST"):
            await member.kick()
    await asyncio.sleep(100)


# console command
@tasks.loop(seconds=1)
async def send_console_msg():
    cc = await aioconsole.ainput()
    await client.get_channel(559613873368465420).send(cc)


@client.event
async def on_ready():
    job_guest.start()
    send_console_msg.start()

    if file_name == "source_test.json":
        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("점검 중이에요!"))
        lprint("Bot is ready for development.")
    if file_name == "source.json":
        await client.change_presence(status=discord.Status.online, activity=discord.Game("@_@"))
        lprint("Bot is ready for service.")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {client.latency:.3f}s")


@client.command(aliases=["리그모집"])
async def set_league_options(ctx):
    if not is_from_guild(ctx):
        return

    args = get_args(ctx.message)
    embed_recruit = discord.Embed(
        title="리그 모집",
        description=' '.join(args[1:]),
        colour=discord.colour.Color(0xFFFFFF)
    )
    embed_recruit.set_footer(text=f"recruited by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    embed_recruit.add_field(name="인원", value=f"0/10")

    msg = await ctx.send(f"<@&{sources['role_id']['TETRA']}><@&{sources['role_id']['TEST']}>", embed=embed_recruit)
    await msg.add_reaction(sources["emoji"]["리그"])

    try:
        while True:
            payload = await client.wait_for('raw_reaction_add', timeout=6.0 * 3600,
                                            check=lambda pay: pay.message_id == msg.id)

            # load reaction
            ch = client.get_channel(payload.channel_id)
            msg = await ch.fetch_message(payload.message_id)
            reaction = discord.utils.get(msg.reactions, emoji=payload.emoji)

            if reaction.emoji.id == 980433210628505670:
                embed_recruit.set_field_at(index=0, name="인원", value=f"{reaction.count - 1}/10")
                await msg.edit(embed=embed_recruit)
                if reaction.count > 2:
                    break

    except asyncio.TimeoutError:
        embed_recruit.set_footer(text="리그 모집이 취소되었습니다.")
        embed_recruit.colour = 0xFF0000
        await msg.edit(embed=embed_recruit)
        return

    user_list = []

    async for member in reaction.users():
        if not member.bot:
            user_list.append(member.display_name)
    chief_list = random.sample(user_list, k=2)

    embed_result = discord.Embed(
        title="리그 모집 완료",
        description=f"**{chief_list[0]}, {chief_list[1]} 님**이 **팀장**입니다!",
        colour=discord.colour.Color(0x00FF00)
    )

    embed_result.set_image(url="https://cdn.discordapp.com/attachments/904390084491624479/991611060907933696/1-5.gif")
    embed_result.add_field(name="선공", value=f"{random.choice(chief_list)}", inline=True)
    embed_result.add_field(name="선픽", value=f"{random.choice(chief_list)}", inline=True)
    embed_result.add_field(name="전장", value=random.choice(sources["vlrt_maps"]), inline=True)
    embed_result.add_field(name="참여자", value=", ".join(user_list), inline=False)
    msg = await ctx.send(embed=embed_result)

    await msg.add_reaction("🏁")
    await msg.add_reaction("🗺️")

    try:
        while True:
            reaction, member = await client.wait_for('reaction_add', timeout=1.0 * 3600,
                                                     check=lambda react, _: react.message.id == msg.id)

            await reaction.remove(member)

            if member != ctx.author and not has_role(member, "ADMIN"):
                await member.send("권한이 부족합니다.\n관리자 또는 리그를 소집한 분만 팀장/맵을 변경할 수 있습니다.")
                continue

            if reaction.emoji == "🏁":
                chief_list = random.sample(user_list, k=2)
                embed_result.description = f"**{chief_list[0]}, {chief_list[1]}** 님이 **팀장**입니다!"
                embed_result.set_field_at(0, name="선공", value=f"{random.choice(chief_list)}", inline=True)
                embed_result.set_field_at(1, name="선픽", value=f"{random.choice(chief_list)}", inline=True)
                await msg.edit(embed=embed_result)

            elif reaction.emoji == "🗺️":
                embed_result.set_field_at(2, name="전장", value=random.choice(sources["vlrt_maps"]), inline=True)
                await msg.edit(embed=embed_result)

    except asyncio.TimeoutError:
        await msg.clear_reactions()


@client.command(aliases=["게스트리셋"])
async def kick_guest(ctx):
    if not is_from_guild(ctx):
        return

    if has_role(ctx.author, "ADMIN"):
        await job_guest(automatic=False)
        await ctx.author.send("게스트 내보내기 처리가 완료되었습니다.")


@client.command(aliases=["도움말"])
async def help(ctx):
    with open("help_command.txt", "r", encoding="utf-8") as text:
        await ctx.author.send(text.read())
    return


@client.command(aliases=["굴려"])
async def roll(ctx):
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


client.run(sources["TOKEN"])

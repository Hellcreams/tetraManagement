import discord
import requests
from discord import app_commands
from discord import ui
from discord.ext import commands


class MemberForm(ui.Modal, title='클랜 테스트멤버 가입 양식'):
    def __init__(self, name, d_id):
        super(MemberForm, self).__init__()
        self.discord_name = name
        self.discord_id = d_id
    vlrt_name = ui.TextInput(label='발로란트 닉네임 및 태그', placeholder="ABCDEFG#KR1")
    server_name = ui.TextInput(label="본 채널에서 사용할 닉네임(영어만)", placeholder="IamABC",
                               min_length=2, max_length=12)
    birth_gender = ui.TextInput(label="생년 및 성별", placeholder="00/남")
    agent = ui.TextInput(label="주 요원", placeholder= "제트, 소바 (또는) 감시자 (또는) 올라운더")
    playtime = ui.TextInput(label="주 접속 시간대", placeholder="평일 20~23시")

    async def on_submit(self, interaction: discord.Interaction):
        # await interaction.response.send_message(f'Thanks for your response, {self.discord_name}!', ephemeral=True)
        await interaction.response.send_message(f"""
        디스코드 이름: `{self.discord_name}`\n
        디스코드 ID : `{self.discord_id}`\n
        발로란트 닉네임 및 태그 : `{self.vlrt_name}`\n
        채널 닉네임 : `{self.server_name}`\n
        생일 및 성별 : `{self.birth_gender}`\n
        주로 플레이하는 요원 : `{self.agent}`\n
        주로 접속하는 시간대 : `{self.playtime}`\n
        """)


class NormalForm(ui.Modal, title="클랜 노말멤버 가입 양식"):
    def __init__(self, name, d_id):
        super(NormalForm, self).__init__()
        self.discord_name = name
        self.discord_id = d_id
    vlrt_name = ui.TextInput(label='발로란트 닉네임 및 태그', placeholder="ABCDEFG#KR1")
    server_name = ui.TextInput(label="본 채널에서 사용할 닉네임", placeholder="IamABC")
    birth_gender = ui.TextInput(label="생년 및 성별", placeholder="01/여")
    invitor = ui.TextInput(label="추천인")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"""
        디스코드 이름: `{self.discord_name}`\n
        디스코드 ID : `{self.discord_id}`\n
        발로란트 닉네임 및 태그 : `{self.vlrt_name}`\n
        채널 닉네임 : `{self.server_name}`\n
        생일 및 성별 : `{self.birth_gender}`\n
        추천인 : `{self.invitor}`\n
        """)



class MyCog(commands.Cog):
    @app_commands.command(name="nanda")
    async def nanda(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MemberForm(interaction.user.name, interaction.id))

    @app_commands.command(name="nanda2")
    async def nanda2(self, interaction: discord.Interaction):
        await interaction.response.send_modal(NormalForm(interaction.user.name, interaction.id))


async def setup(bot: commands.bot):
    await bot.add_cog(MyCog(bot))


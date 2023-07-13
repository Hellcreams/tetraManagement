import discord
from discord import ui
from discord.ext import commands, tasks

intents = discord.Intents().all()
client = commands.Bot(intents=intents, command_prefix="*!", help_command=None)

# Read Token
file_name = "token.man"
with open(file_name, 'r', encoding="utf-8") as file:
    TOKEN = file.read()


class Questionnaire(ui.Modal, title='클랜 테스트멤버 가입 양식'):
    def __init__(self, name, id):
        super(Questionnaire, self).__init__()
        self.discord_name = name
        self.discord_id = id
    answer = ui.TextInput(label='발로란트 닉네임 및 태그')
    server_name = ui.TextInput(label="본 채널에서 사용할 닉네임")
    birth_gender = ui.TextInput(label="생년 및 성별")
    agent = ui.TextInput(label="주 요원")
    playtime = ui.TextInput(label="주 접속 시간대")

    async def on_submit(self, interaction: discord.Interaction):
        # await interaction.response.send_message(f'Thanks for your response, {self.discord_name}!', ephemeral=True)
        await interaction.response.send_message(f"""
        디스코드 이름: `{self.discord_name}`
        디스코드 ID : `{self.discord_id}`
        발로란트 닉네임 및 태그 : `{self.answer}`
        채널 닉네임 : `{self.server_name}`
        생일 및 성별 : `{self.birth_gender}`
        주로 플레이하는 요원 : `{self.agent}`
        주로 접속하는 시간대 : `{self.playtime}`
        """)


@client.event
async def on_ready():
    try:
        await client.load_extension('cogs.addon')
    except discord.ext.commands.errors.ExtensionError:
        print("No Extension.")

    print("Bot Online.")


@client.tree.command(name="what", description="testing")
async def what(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


@client.tree.command(name="nani", description="testing")
async def nani(interaction: discord.Interaction):
    await interaction.response.send_modal(Questionnaire(interaction.user.name, interaction.id))


client.run(TOKEN)

from discord import app_commands
from discord.ext import commands
from funcs import *

class Askgpt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='askgpt', description='ask chatgpt a question')
    async def askgpt(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        await gpt(interaction, prompt, [
        {"role": "system", "content": "You are a helpful chatbot. Respond to the prompt as best as possible."},
        {"role": "user", "content": "Here is the prompt: '{}'".format(prompt)}
    ])

    @app_commands.command(name='ask12yo', description='ask a sarcastic 12yo a question')
    async def ask12yo(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        await gpt(interaction, prompt, [
            {"role": "system", "content": "You are a sarcastic 12 year old assistant who answers questions. Do not hesitate to be mean or make insults, especially related to monkeys, low intelligence, race, body weight, and anything else that might strike a nerve."},
            {"role": "user", "content": "Here is the prompt: '{}'".format(prompt)}
        ])

async def setup(client):
    await client.add_cog(Askgpt(client))

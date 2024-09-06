from discord import app_commands
from discord.ext import commands
from funcs import *


class Summarize(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='summarize', description='analyze text')
    async def summarize(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        await gpt(interaction, text, [
            {"role": "system", "content": "You are an english professor who will summarize a selection of text in a few sentences, including all key details. Keep in mind that there may be spelling errors or cut off words so try your best to interpret the text."},
            {"role": "user", "content": "Here is the text: '{}'".format(text)}
        ])

    @app_commands.command(name='summarizefile', description='summarize text from an image or pdf')
    async def summarizefile(self, interaction: discord.Interaction, file: discord.Attachment):
        await interaction.response.defer()
        text = await init_scan(interaction, file)
        if text != 'failed':
            await gpt(interaction, text, [
            {"role": "system", "content": "You are an english professor who will summarize a selection of text in a few sentences, including all key details. Keep in mind that there may be spelling errors or cut off words so try your best to interpret the text."},
            {"role": "user", "content": "Here is the text: '{}'".format(text)}
        ])

async def setup(client):
    await client.add_cog(Summarize(client))
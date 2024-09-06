from discord import app_commands
from discord.ext import commands
from funcs import *

class Analyze(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='analyze', description='analyze text')
    async def analyze(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        await gpt(interaction, text, [
                {"role": "system", "content": "You are an english professor who will analyze a selection of text in a few sentences. Look for any literary devices and author's craft, as well as any other notable features of the text. Keep in mind that there may be spelling errors or cut off words so try your best to interpret the text."},
                {"role": "user", "content": "Here is the text: '{}'".format(text)}
            ])

    @app_commands.command(name='analyzefile', description='analyze text from an image or pdf')
    async def analyzefile(self, interaction: discord.Interaction, file: discord.Attachment):
        await interaction.response.defer()
        text = await init_scan(interaction, file)
        if text != 'failed':
            await gpt(interaction, text, [
                {"role": "system", "content": "You are an english professor who will analyze a selection of text in a few sentences. Look for any literary devices and author's craft, as well as any other notable features of the text. Keep in mind that there may be spelling errors or cut off words so try your best to interpret the text."},
                {"role": "user", "content": "Here is the text: '{}'".format(text)}
            ])

async def setup(client):
    await client.add_cog(Analyze(client))

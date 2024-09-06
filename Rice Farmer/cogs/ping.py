import discord
from discord import app_commands
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command(name='ping', description='check if bot is working')
    async def ping(self, interaction: discord.Interaction):

        await interaction.response.defer()

        await interaction.followup.send('"never stop chasing that bag (of rice)"\n - Rice Farmer')


async def setup(client):
    await client.add_cog(Ping(client))

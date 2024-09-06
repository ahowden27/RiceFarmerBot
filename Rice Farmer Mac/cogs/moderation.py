import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command(name='purge', description='clears messages')
    async def purge(self, interaction: discord.Interaction, count: int):

        await interaction.response.defer()

        if interaction.user.guild_permissions.manage_messages:

            await interaction.channel.purge(limit=count)
            await interaction.followup.send('{count} messages have been purged.')

        else:
            await interaction.followup.send('You do not have permission to use this command.')


    @app_commands.command(name='sync', description='syncs commands')
    async def sync(self, interaction: discord.Interaction):

        if interaction.user.guild_permissions.administrator:

            await interaction.response.defer()
            synced = await self.client.tree.sync()
            await interaction.followup.send(f"Synced {len(synced)} command(s).")

        else:
            await interaction.response.send('You do not have permission to use this command.')


async def setup(client):
    await client.add_cog(Moderation(client))

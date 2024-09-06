import discord
from discord import app_commands
from discord.ext import commands
import json


class Credits(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command(name='credits', description='displays credit info')
    async def credits(self, interaction: discord.Interaction):

        await interaction.response.defer()

        try:
            with open(r'/Users/misterrobot/Desktop/Programming/Rice Farmer/userlog.json', 'r') as file:
                user_profiles = json.load(file)

            used = user_profiles[str(interaction.user.id)]['used']
            available = user_profiles[str(interaction.user.id)]['available']

            if used > available:
                used = available

            await interaction.followup.send(f"You have used {round(used, 2)} out of {available} available credits.")

        except:
            await interaction.followup.send("This command is exclusive to subscribers. See https://discord.com/channels/1118288278622310433/1149856144890794106 to learn more.")


async def setup(client):
    await client.add_cog(Credits(client))
import discord
from discord import app_commands
from discord.ext import commands
import json
from funcs import *


class Subscriptions(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command(name='activate')
    async def activate(self, interaction: discord.Interaction):

        await interaction.response.defer()

        if not has_subscription(interaction):
            await interaction.followup.send(
                "This command is exclusive to subscribers. See https://discord.com/channels/1118288278622310433/1149856144890794106 to learn more.")
            return

        try:
            create_profile(interaction.user.id, get_tier(interaction))

        except Exception as e:
            print(e)

        await interaction.followup.send('Subscription successfully activated.')


    @app_commands.command(name='setup')
    async def setup(self, interaction: discord.Interaction, uid: str, available: int):

        await interaction.response.defer()

        if interaction.user.guild_permissions.administrator:
            try:
                with open('userlog.json', 'r') as file:
                    user_profiles = json.load(file)
            except:
                user_profiles = {}

            if uid not in user_profiles:
                user_profiles[uid] = {'used': 0, 'available': available}

                with open('userlog.json', 'w') as outfile:
                    json.dump(user_profiles, outfile, indent=4)
            else:
                await interaction.followup.send(f"User {uid} already has a subscription.")

            await interaction.followup.send(f"Subscription successfully created for user {uid} with {available} credits.")
        else:
            await interaction.followup.send("You do not have permission to use this command.")


    @app_commands.command(name='modify')
    async def modify(self, interaction: discord.Interaction, uid: str, usedoravailable: str, amount: int):

        await interaction.response.defer()

        if interaction.user.guild_permissions.administrator:
            try:
                with open('userlog.json', 'r') as file:
                    user_profiles = json.load(file)
            except:
                user_profiles = {}

            if uid not in user_profiles:
                interaction.followup.send(f"User {uid} does not have a subscription.")
            else:
                if usedoravailable in ['used', 'available']:
                    if usedoravailable == 'used':
                        user_profiles[uid]['used'] = amount

                        with open('userlog.json', 'w') as outfile:
                            json.dump(user_profiles, outfile, indent=4)

                    elif usedoravailable == 'available':
                        user_profiles[uid]['available'] = amount

                        with open('userlog.json', 'w') as outfile:
                            json.dump(user_profiles, outfile, indent=4)

                    await interaction.followup.send(f"Successfully set {usedoravailable} credits to {amount} for user {uid}.")

                else:
                    await interaction.followup.send("Typo; please try again.")

        else:
            await interaction.followup.send("You do not have permission to use this command.")


    @app_commands.command(name='trial')
    async def trial(self, interaction: discord.Interaction, uid: str, available: int):

        await interaction.response.defer()

        if interaction.user.guild_permissions.administrator:
            try:
                with open('userlog.json', 'r') as file:
                    user_profiles = json.load(file)
            except:
                user_profiles = {}

            if uid not in user_profiles:
                user_profiles[uid] = {'used': 0, 'available': available}

            with open('userlog.json', 'w') as outfile:
                json.dump(user_profiles, outfile, indent=4)

            await interaction.followup.send(
                f"Trial subscription successfully created for user {uid} with {available} credits.")
        else:
            await interaction.followup.send("You do not have permission to use this command.")


async def setup(client):
    await client.add_cog(Subscriptions(client))

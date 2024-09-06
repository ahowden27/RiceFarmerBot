import discord
from discord import app_commands
from discord.ext import commands
import openai
from creds import org, api_key
from funcs import update_usage, has_credits, has_subscription


class Dalle(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command(name='dalle', description='generate an image')
    async def dalle(self, interaction: discord.Interaction, prompt: str):

        await interaction.response.defer()

        if not has_subscription(interaction):
            await interaction.followup.send(
                "This command is exclusive to subscribers. See https://discord.com/channels/1118288278622310433/1149856144890794106 to learn more.")
            return

        if not has_credits(str(interaction.user.id)):
            await interaction.followup.send(
                "You have no remaining credits. See https://discord.com/channels/1118288278622310433/1149856144890794106 to learn more.")
            return

        try:
            response = self.openai(prompt)
            await interaction.followup.send(response['data'][0]['url'])
            update_usage(userid=interaction.user.id, itokens=0, otokens=1, model='dalle')
        except:
            await interaction.followup.send('Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed by our safety system.')


    def openai(self, prompt):
        organization = org
        openai.api_key = api_key
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )

        return response


async def setup(client):
    await client.add_cog(Dalle(client))

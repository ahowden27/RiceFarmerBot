import discord
from discord import app_commands
from discord.ext import commands
import random


class Inspiration(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.quotes = ['"The smaller the circle, the better the people"',
                       '"People only spectate when you are on the verge of victory"',
                       "\"You don't get mats from breaking someone else's buildings\"",
                       "\"The people with scars are the strongest\"",
                       "\"You can't expect high ground if you don't take the time to farm mats\"",
                       "\"Just because you' a're in the storm doesn't mean the game is over\"",
                       "\"Life is like a sky base, people want to knock you down when you're at the top\"",
                       "\"If she was never with you in the storm then why take her to the final circle\"",
                       "\"Everyone goes back to the lobby in the end, even the winners\"",
                       "\"The bigger the circle the more enemies there are\"",
                       "\"Just because it’s legendary doesn’t mean it’s the best\"",
                       "\"Someone can change their skin as many times as they want, but at the end of the day they are still the same player on the inside\"",
                       "\"Sometimes even the best get lost in the storm\"",
                       "\"Even opened chests shined at one point\"",
                       "\"You can have a full friends list but still have an empty lobby\"",
                       "\"If you weren't there fighting with me, then don't come when I'm looting\"",
                       "\"If you camp all game, how do you expect to get good loot?\"",
                       "\"No matter how many shields you have, the storm can still hurt\"",
                       "\"Unopened chests shine the brightest\"",
                       "\"Metal takes longer to build, but it always lasts the longest\"",
                       "\"You can buy as many vbucks as you want, but true skill will always succeed\""]


    @app_commands.command(name='inspiration', description='for when the times get tough')
    async def inspiration(self, interaction: discord.Interaction):


        await interaction.response.defer()

        await interaction.followup.send(self.quotes[random.randint(0, len(self.quotes))])


async def setup(client):
    await client.add_cog(Inspiration(client))

from discord import app_commands
from discord.ext import commands
from funcs import *

class Lawsummarize(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='lawsummarize', description='generate summaries for law articles')
    async def summarize(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        await gpt(interaction, text, [
                {"role": "system", "content": """
Give me the following information, using the phrases in quotes as the headers with the content in parenthesis:

“Date of article”
(State the date of the article)

“Author of the article”
(Author)

“Summary”
(create a 3-6 sentence summary of an article. Answer the following questions in the summary, and include the questions in the sentences: 
who was involved, what did they do, how did they do it, when did the crime take place, where did the crime take place, why did they do it.)

“Questions”
(What criminal law questions do you have after having read this news article?)
                """},
                {"role": "user", "content": "Here is the article: '{}'".format(text)}
            ])

    @app_commands.command(name='lawsummarizefile', description='generate summaries for law articles from an image or pdf')
    async def summarizefile(self, interaction: discord.Interaction, file: discord.Attachment):
        await interaction.response.defer()
        text = await init_scan(interaction, file)
        if text != 'failed':
            await gpt(interaction, text, [
                {"role": "system", "content": "You are an 8th grader in law class. Your assignment is to create a 3-6 sentence summary of an article. Answer the following questions in the summary, and include the questions in the sentences: who was involved, what did they do, how did they do it, when did the crime take place, where did the crime take place, why did they do it."},
                {"role": "user", "content": "Here is the article: '{}'".format(text)}
            ])

async def setup(client):
    await client.add_cog(Lawsummarize(client))

import discord
from discord import app_commands
from discord.ext import commands
import matplotlib.pyplot as plt
import numpy as np

class Graph(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='graph', description='graph an equation')
    async def graph(self, interaction: discord.Interaction, equation: str, xmin: int, xmax: int):
        await interaction.response.defer()
        equation = equation.replace('^', '**')
        try:
            x = np.linspace(xmin, xmax, 400)
            y = eval(equation, {"__builtins__": None}, {"x": x, "ln": np.log, "log": np.log10, "sin": np.sin, "cos": np.cos, "tan": np.tan, "abs": np.abs})
            plt.figure(figsize=(6, 4))
            plt.plot(x, y)
            plt.title(f'Graph of {equation}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)

            plt.savefig('graph.png')

            await interaction.followup.send(file=discord.File('graph.png'))
        except Exception as e:
            await interaction.followup.send(f'Error: {e}')

async def setup(client):
    await client.add_cog(Graph(client))

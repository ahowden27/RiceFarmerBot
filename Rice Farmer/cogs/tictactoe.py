import discord
from discord import app_commands
from discord.ext import commands
import re


class TicTacToe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.active_games = {}


    def display_board(self, game):
        print(game)
        board = ""
        for i in range(0, 9, 3):
            row = " | ".join(game[i:i + 3])
            board += f"{row}\n"
            if i < 6:
                board += "---------\n"
        return f"```\n{board}```"


    def check_win(self, game):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                           (0, 3, 6), (1, 4, 7), (2, 5, 8),
                           (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if (game[condition[0]] == game[condition[1]] == game[condition[2]]) and (game[condition[0]] != " "):
                return True
        if " " not in game:
            return "draw"
        return False


    @app_commands.command(name='tictactoe', description='play tictactoe')
    async def tictactoe(self, interaction: discord.Interaction, opponent: str):

        await interaction.response.defer()

        try:
            opponent = int(re.search(r'\d+', opponent).group())
        except:
            await interaction.followup.send('Please @ your opponent in the parameter.')

        user_exists = any(member.id == opponent for member in interaction.guild.members)
        if not user_exists:
            await interaction.followup.send("Cannot find player.")
            return

        if interaction.user.id in self.active_games:
            await interaction.followup.send("You are already in a game. Finish it before starting a new one.")
            return
        elif opponent in self.active_games:
            await interaction.followup.send("This player is already in a game. Finish it before starting a new one.")
            return

        game_board = [" "] * 9
        game_message = await interaction.followup.send(f"Tic-Tac-Toe Game - Current Player: <@{interaction.user.id}>\n" + self.display_board(game_board))

        for i in range(1, 10):
            await game_message.add_reaction(f"{i}\N{COMBINING ENCLOSING KEYCAP}")

        self.active_games[interaction.user.id] = {
            "board": game_board,
            "current_player": interaction.user.id,
            "message": game_message,
            "user": interaction.user.id,
            "opponent": opponent
        }

    @app_commands.command(name='deletegame', description='delete your tictactoe game')
    async def deletegame(self, interaction: discord.Interaction):

        await interaction.response.defer()

        if interaction.user.id in self.active_games:
            self.active_games.pop(interaction.user.id)
            await interaction.followup.send("Game successfully deleted.")
        else:
            await interaction.followup.send("No game found.")


    @app_commands.command(name='cleargames', description='clears all tictactoe games')
    async def deletegame(self, interaction: discord.Interaction):

        await interaction.response.defer()

        if interaction.user.id == 472088550813204481:
            self.active_games = {}
            await interaction.followup.send("All games cleared.")
        else:
            await interaction.followup.send("You do not have permission.")


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        if user.id == 1149870249781502063:
            return

        game_data = self.active_games.get(user.id)

        if game_data is None:
            for game in self.active_games.values():
                if game["opponent"] == user.id:
                    game_data = game

        if game_data is None or reaction.message.id != game_data["message"].id:
            return

        move = int(str(reaction.emoji)[0])

        if 1 <= move <= 9 and game_data["board"][move - 1] == " " and game_data["current_player"] == user.id:
            print('good')
            if game_data["current_player"] == game_data["user"]:
                game_data["board"][move - 1] = "X"
            else:
                game_data["board"][move - 1] = "O"
            winner = self.check_win(game_data["board"])
            if winner:
                if winner == "draw":
                    await game_data["message"].edit(content="It's a draw!\n" + self.display_board(game_data["board"]))
                else:
                    await game_data["message"].edit(content=f"<@{game_data['current_player']}> wins!\n" + self.display_board(game_data["board"]))
                del self.active_games[user.id]
            else:
                print('arrived')
                if game_data["current_player"] == game_data["user"]:
                    game_data["current_player"] = game_data["opponent"]
                else:
                    game_data["current_player"] = game_data["user"]
                await game_data["message"].edit(content=f"Tic-Tac-Toe Game - Current Player: <@{game_data['current_player']}>\n" + self.display_board(game_data["board"]))


async def setup(client):
    await client.add_cog(TicTacToe(client))

import discord
from discord.ext import commands
from discord import app_commands

# Process「」Class
class TicTacToeButton(discord.ui.Button):
    def __init__(self, x: int, y: int):
        # Settings， y 
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view
        
        # 【RuleCheck】Confirm，「」
        if interaction.user != view.current_player:
            await interaction.response.send_message("！。", ephemeral=True)
            return

        #  1  2，Graph
        if view.current_player == view.player1:
            self.style = discord.ButtonStyle.danger # 
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.player1
            view.current_player = view.player2 # 
        else:
            self.style = discord.ButtonStyle.success # 
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.player2
            view.current_player = view.player1 # 

        # Check
        winner = view.check_winner()
        if winner:
            # ，
            for child in view.children:
                child.disabled = True
            content = f"[PARTY] ！ {winner.mention} ！"
            await interaction.response.edit_message(content=content, view=view)
        # Check
        elif view.is_tie():
            content = "[HANDSHAKE] ！，！"
            await interaction.response.edit_message(content=content, view=view)
        # Continue
        else:
            content = f"[GAME] ！\n {view.current_player.mention} "
            await interaction.response.edit_message(content=content, view=view)

# Process「」Class
class TicTacToeView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=180) # 3 AutoCancel
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        
        #  3x3  9 
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_winner(self):
        # Check、、Connection
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] and b[i][0] is not None: return b[i][0]
            if b[0][i] == b[1][i] == b[2][i] and b[0][i] is not None: return b[0][i]
        if b[0][0] == b[1][1] == b[2][2] and b[0][0] is not None: return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] is not None: return b[0][2]
        return None
        
    def is_tie(self):
        # Check
        for row in self.board:
            if None in row: return False
        return True

# CommandBot Cog Class
class GameTicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_tictactoe", description="！")
    @app_commands.describe(opponent="")
    async def play_tictactoe(self, interaction: discord.Interaction, opponent: discord.Member):
        # 
        if opponent.bot:
            await interaction.response.send_message("Bot，！", ephemeral=True)
            return
        if opponent == interaction.user:
            await interaction.response.send_message("！！", ephemeral=True)
            return
        
        # InitializeInterface
        view = TicTacToeView(interaction.user, opponent)
        content = f"[GAME] ！\n{interaction.user.mention} (X) VS {opponent.mention} (O)\n {interaction.user.mention} ！"
        await interaction.response.send_message(content=content, view=view)

# LoadModule
async def setup(bot):
    await bot.add_cog(GameTicTacToe(bot))
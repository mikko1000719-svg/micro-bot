import discord
from discord import app_commands
from discord.ext import commands

class GomokuView(discord.ui.View):
    def __init__(self, p1: discord.Member, p2: discord.Member):
        super().__init__(timeout=300)  # 5
        self.p1 = p1  # 🔵 
        self.p2 = p2  # ⬛ 
        self.current_turn = p1  # Default
        
        # Initialize 5x5  ( Discord Limit， 5x5  6x6 ，)
        # 0: , 1: 🔵, 2: ⬛
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.game_over = False
        
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        for r in range(5):
            for c in range(5):
                #  5x5 
                button = discord.ui.Button(
                    style=discord.ButtonStyle.secondary,
                    label=self.get_label(self.board[r][c]),
                    row=r,
                    custom_id=f"gomoku_{r}_{c}"
                )
                button.callback = self.make_callback(r, c)
                self.add_item(button)

    def get_label(self, val):
        if val == 1:
            return "🔵"
        elif val == 2:
            return "⬛"
        return "·"

    def make_callback(self, r, c):
        async def callback(interaction: discord.Interaction):
            if self.game_over:
                await interaction.response.send_message("！", ephemeral=True)
                return

            # Check
            if interaction.user != self.current_turn:
                await interaction.response.send_message("！", ephemeral=True)
                return

            # Check
            if self.board[r][c] != 0:
                await interaction.response.send_message("！", ephemeral=True)
                return

            # 
            player_val = 1 if self.current_turn == self.p1 else 2
            self.board[r][c] = player_val

            # CheckCondition (Connection)
            if self.check_win(player_val):
                self.game_over = True
                self.update_buttons()
                winner_name = self.p1.name if player_val == 1 else self.p2.name
                winner_icon = "🔵 " if player_val == 1 else "⬛ "
                await interaction.response.edit_message(
                    content=f"[PARTY] ！ {winner_icon} ({winner_name}) ！",
                    view=self
                )
                return

            # 
            self.current_turn = self.p2 if self.current_turn == self.p1 else self.p1
            self.update_buttons()
            
            turn_icon = "🔵 " if self.current_turn == self.p1 else "⬛ "
            await interaction.response.edit_message(
                content=f"[GAME] \n {turn_icon} ({self.current_turn.mention}) ！",
                view=self
            )

        return callback

    def check_win(self, val):
        #  3  5 Connection ( 5x5 ，Connection 4  5 )
        b = self.board
        n = 5
        target = 4  # 5x5 Connection 4 ，Requirement
        
        # Check、、
        for r in range(n):
            for c in range(n):
                if b[r][c] == val:
                    # Check
                    if c + target <= n and all(b[r][c+i] == val for i in range(target)):
                        return True
                    # Check
                    if r + target <= n and all(b[r+i][c] == val for i in range(target)):
                        return True
                    # Check
                    if r + target <= n and c + target <= n and all(b[r+i][c+i] == val for i in range(target)):
                        return True
                    # Check
                    if r - target >= -1 and c + target <= n and all(b[r-i][c+i] == val for i in range(target)):
                        return True
        return False

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gomoku", description=" ( vs )")
    @app_commands.describe(opponent="")
    async def gomoku(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot:
            await interaction.response.send_message("Bot！", ephemeral=True)
            return
        if opponent == interaction.user:
            await interaction.response.send_message("！", ephemeral=True)
            return

        view = GomokuView(p1=interaction.user, p2=opponent)
        await interaction.response.send_message(
            f"⚔️ ！\n🔵 ：{interaction.user.mention} vs ⬛ ：{opponent.mention}\n 🔵 ！",
            view=view
        )

async def setup(bot):
    await bot.add_cog(Games(bot))
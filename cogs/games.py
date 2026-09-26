# -*- coding: utf-8 -*-
import discord
from discord import app_commands
from discord.ext import commands

class GomokuView(discord.ui.View):
    def __init__(self, p1: discord.Member, p2: discord.Member):
        super().__init__(timeout=300)  # 5 minutes
        self.p1 = p1  # Blue
        self.p2 = p2  # Black
        self.current_turn = p1  # Default

        # Initialize 5x5 board (Discord Limit, 5x5 instead of 6x6)
        # 0: empty, 1: Blue, 2: Black
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.game_over = False

        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        for r in range(5):
            for c in range(5):
                # Create 5x5 buttons
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
            return "[BLUE]"
        elif val == 2:
            return "[BLACK]"
        return "[ ]"

    def make_callback(self, r, c):
        async def callback(interaction: discord.Interaction):
            if self.game_over:
                await interaction.response.send_message("[ERROR] Game is already over!", ephemeral=True)
                return

            # Check turn
            if interaction.user != self.current_turn:
                await interaction.response.send_message("[ERROR] Not your turn!", ephemeral=True)
                return

            # Check cell
            if self.board[r][c] != 0:
                await interaction.response.send_message("[ERROR] Cell already occupied!", ephemeral=True)
                return

            # Place piece
            player_val = 1 if self.current_turn == self.p1 else 2
            self.board[r][c] = player_val

            # Check win condition (Connect 4 in 5x5)
            if self.check_win(player_val):
                self.game_over = True
                self.update_buttons()
                winner_name = self.p1.name if player_val == 1 else self.p2.name
                winner_icon = "[BLUE]" if player_val == 1 else "[BLACK]"
                await interaction.response.edit_message(
                    content=f"[WINNER] {winner_icon} ({winner_name}) wins!",
                    view=self
                )
                return

            # Switch turn
            self.current_turn = self.p2 if self.current_turn == self.p1 else self.p1
            self.update_buttons()

            turn_icon = "[BLUE]" if self.current_turn == self.p1 else "[BLACK]"
            await interaction.response.edit_message(
                content=f"[GAME] Current turn: {turn_icon} ({self.current_turn.mention})",
                view=self
            )

        return callback

    def check_win(self, val):
        # Check 4 connections in 5x5 board (connect 4 to win in 5x5)
        b = self.board
        n = 5
        target = 4  # Connect 4 to win in 5x5

        # Check horizontal, vertical, diagonal
        for r in range(n):
            for c in range(n):
                if b[r][c] == val:
                    # Check horizontal
                    if c + target <= n and all(b[r][c+i] == val for i in range(target)):
                        return True
                    # Check vertical
                    if r + target <= n and all(b[r+i][c] == val for i in range(target)):
                        return True
                    # Check diagonal
                    if r + target <= n and c + target <= n and all(b[r+i][c+i] == val for i in range(target)):
                        return True
                    # Check anti-diagonal
                    if r - target >= -1 and c + target <= n and all(b[r-i][c+i] == val for i in range(target)):
                        return True
        return False

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gomoku", description="Play Gomoku (5x5 Connect 4)")
    @app_commands.describe(opponent="Choose your opponent")
    async def gomoku(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot:
            await interaction.response.send_message("[ERROR] Cannot play against bots!", ephemeral=True)
            return
        if opponent == interaction.user:
            await interaction.response.send_message("[ERROR] Cannot play against yourself!", ephemeral=True)
            return

        view = GomokuView(p1=interaction.user, p2=opponent)
        await interaction.response.send_message(
            f"[GAME START] Gomoku Match!\n[BLUE]: {interaction.user.mention} vs [BLACK]: {opponent.mention}\n[BLUE] goes first!",
            view=view
        )

async def setup(bot):
    await bot.add_cog(Games(bot))
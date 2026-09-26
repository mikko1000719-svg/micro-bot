import discord
from discord import app_commands
from discord.ext import commands

class GomokuView(discord.ui.View):
    def __init__(self, p1: discord.Member, p2: discord.Member):
        super().__init__(timeout=300)  # 5分鐘超時
        self.p1 = p1  # 🔵 藍方
        self.p2 = p2  # ⬛ 黑方
        self.current_turn = p1  # 預設藍方先手
        
        # 初始化 5x5 棋盤 (為了 Discord 畫面排版與按鈕限制，先以 5x5 或 6x6 互動按鈕為主，可自行擴充)
        # 0: 空白, 1: 🔵藍方, 2: ⬛黑方
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.game_over = False
        
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        for r in range(5):
            for c in range(5):
                # 建立 5x5 的按鈕網格
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
                await interaction.response.send_message("遊戲已經結束囉！", ephemeral=True)
                return

            # 檢查是否輪到該玩家
            if interaction.user != self.current_turn:
                await interaction.response.send_message("還沒輪到你或是你不是對局玩家！", ephemeral=True)
                return

            # 檢查格子是否已被佔用
            if self.board[r][c] != 0:
                await interaction.response.send_message("這裡已經有棋子了！", ephemeral=True)
                return

            # 下棋
            player_val = 1 if self.current_turn == self.p1 else 2
            self.board[r][c] = player_val

            # 檢查勝利條件 (簡化的連線判定)
            if self.check_win(player_val):
                self.game_over = True
                self.update_buttons()
                winner_name = self.p1.name if player_val == 1 else self.p2.name
                winner_icon = "🔵 藍方" if player_val == 1 else "⬛ 黑方"
                await interaction.response.edit_message(
                    content=f"[PARTY] 遊戲結束！恭喜 {winner_icon} ({winner_name}) 獲勝！",
                    view=self
                )
                return

            # 切換回合
            self.current_turn = self.p2 if self.current_turn == self.p1 else self.p1
            self.update_buttons()
            
            turn_icon = "🔵 藍方" if self.current_turn == self.p1 else "⬛ 黑方"
            await interaction.response.edit_message(
                content=f"[GAME] 五子棋對戰中\n輪到 {turn_icon} ({self.current_turn.mention}) 下棋！",
                view=self
            )

        return callback

    def check_win(self, val):
        # 簡單的 3 子或 5 子連線判定邏輯 (以 5x5 為例，連線 4 子或 5 子)
        b = self.board
        n = 5
        target = 4  # 5x5 棋盤通常連線 4 子即獲勝，可依需求調整
        
        # 檢查橫排、直排、斜排
        for r in range(n):
            for c in range(n):
                if b[r][c] == val:
                    # 檢查右
                    if c + target <= n and all(b[r][c+i] == val for i in range(target)):
                        return True
                    # 檢查下
                    if r + target <= n and all(b[r+i][c] == val for i in range(target)):
                        return True
                    # 檢查右下斜
                    if r + target <= n and c + target <= n and all(b[r+i][c+i] == val for i in range(target)):
                        return True
                    # 檢查右上斜
                    if r - target >= -1 and c + target <= n and all(b[r-i][c+i] == val for i in range(target)):
                        return True
        return False

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gomoku", description="與朋友進行一場五子棋對戰 (藍 vs 黑)")
    @app_commands.describe(opponent="你的對戰對手")
    async def gomoku(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot:
            await interaction.response.send_message("你不能跟機器人對戰！", ephemeral=True)
            return
        if opponent == interaction.user:
            await interaction.response.send_message("你不能自己跟自己對戰！", ephemeral=True)
            return

        view = GomokuView(p1=interaction.user, p2=opponent)
        await interaction.response.send_message(
            f"⚔️ 五子棋對戰開始！\n🔵 藍方：{interaction.user.mention} vs ⬛ 黑方：{opponent.mention}\n輪到 🔵 藍方先手！",
            view=view
        )

async def setup(bot):
    await bot.add_cog(Games(bot))
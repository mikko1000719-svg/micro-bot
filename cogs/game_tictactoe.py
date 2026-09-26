import discord
from discord.ext import commands
from discord import app_commands

# 負責處理每一個「按鈕」的類別
class TicTacToeButton(discord.ui.Button):
    def __init__(self, x: int, y: int):
        # 設定按鈕為灰色，並根據 y 決定按鈕在第幾排
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view
        
        # 【規則檢查】確認按按鈕的人，是不是「現在輪到的玩家」
        if interaction.user != view.current_player:
            await interaction.response.send_message("還沒輪到你喔！請等對手下棋。", ephemeral=True)
            return

        # 根據是玩家 1 還是玩家 2，改變按鈕顏色跟圖案
        if view.current_player == view.player1:
            self.style = discord.ButtonStyle.danger # 紅色
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.player1
            view.current_player = view.player2 # 換對手
        else:
            self.style = discord.ButtonStyle.success # 綠色
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.player2
            view.current_player = view.player1 # 換對手

        # 檢查是否有人獲勝
        winner = view.check_winner()
        if winner:
            # 有人贏了，把所有按鈕鎖死
            for child in view.children:
                child.disabled = True
            content = f"[PARTY] 遊戲結束！恭喜 {winner.mention} 獲勝！"
            await interaction.response.edit_message(content=content, view=view)
        # 檢查是否平手
        elif view.is_tie():
            content = "[HANDSHAKE] 遊戲結束！棋盤滿了，雙方平手！"
            await interaction.response.edit_message(content=content, view=view)
        # 繼續遊戲
        else:
            content = f"[GAME] 圈圈叉叉對戰中！\n現在輪到 {view.current_player.mention} 下棋"
            await interaction.response.edit_message(content=content, view=view)

# 負責處理「整個遊戲盤面」的類別
class TicTacToeView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=180) # 3 分鐘沒人按自動取消
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        
        # 產生 3x3 共 9 個按鈕
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_winner(self):
        # 檢查橫排、直排、斜線是否有連線
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] and b[i][0] is not None: return b[i][0]
            if b[0][i] == b[1][i] == b[2][i] and b[0][i] is not None: return b[0][i]
        if b[0][0] == b[1][1] == b[2][2] and b[0][0] is not None: return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] is not None: return b[0][2]
        return None
        
    def is_tie(self):
        # 檢查是否還有空位
        for row in self.board:
            if None in row: return False
        return True

# 負責把指令註冊到機器人的 Cog 類別
class GameTicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_tictactoe", description="與另一位真實玩家對戰圈圈叉叉！")
    @app_commands.describe(opponent="選擇你要挑戰的玩家")
    async def play_tictactoe(self, interaction: discord.Interaction, opponent: discord.Member):
        # 防呆機制
        if opponent.bot:
            await interaction.response.send_message("你不能跟機器人玩喔，請選擇一個真實玩家！", ephemeral=True)
            return
        if opponent == interaction.user:
            await interaction.response.send_message("你不能跟自己玩啦！去找個朋友挑戰吧！", ephemeral=True)
            return
        
        # 初始化遊戲介面
        view = TicTacToeView(interaction.user, opponent)
        content = f"[GAME] 圈圈叉叉遊戲開始！\n{interaction.user.mention} (X) VS {opponent.mention} (O)\n現在輪到 {interaction.user.mention} 先下！"
        await interaction.response.send_message(content=content, view=view)

# 載入模組的必要函式
async def setup(bot):
    await bot.add_cog(GameTicTacToe(bot))
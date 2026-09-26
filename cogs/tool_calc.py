import discord
import ast
from discord.ext import commands
from discord import app_commands

class ToolCalc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="calc", description="計算簡單的數學算式（支援 +, -, *, /, 括號）")
    @app_commands.describe(expression="例如: (5 + 3) * 4")
    async def calc(self, interaction: discord.Interaction, expression: str):
        # 安全解析數學算式的函數
        allowed_operators = {
            ast.Add: lambda a, b: a + b,
            ast.Sub: lambda a, b: a - b,
            ast.Mult: lambda a, b: a * b,
            ast.Div: lambda a, b: a / b,
            ast.USub: lambda a: -a
        }

        def eval_expr(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            elif isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
                return allowed_operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
            elif isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
                return allowed_operators[type(node.op)](eval_expr(node.operand))
            else:
                raise ValueError("不支援的運算式")

        try:
            node = ast.parse(expression, mode='eval')
            result = eval_expr(node.body)
            
            embed = discord.Embed(title="🔢 計算結果", color=discord.Color.blue())
            embed.add_field(name="算式", value=f"`{expression}`", inline=False)
            embed.add_field(name="答案", value=f"**{result}**", inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception:
            await interaction.response.send_message("[ERROR] 計算失敗！請確認您的數學算式格式是否正確（僅支援基本加減乘除與數字）。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ToolCalc(bot))
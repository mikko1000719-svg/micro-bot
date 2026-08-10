import os
import json
import discord
from discord import app_commands
from discord.ext import commands

DATA_FILE = "stocks.json"

class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stocks = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.stocks, f, indent=4)

    @app_commands.command(name="增加股票的公司", description="新增一家上市公司")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_company(self, interaction: discord.Interaction, code: str, name: str, initial_price: float):
        code = code.upper()
        self.stocks[code] = {"name": name, "price": initial_price}
        self.save_data()
        await interaction.response.send_message(f"📈 成功新增公司 `{code}` ({name})，初始股價: ${initial_price}", ephemeral=True)

    @app_commands.command(name="下架股票的公司", description="下架指定上市公司")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_company(self, interaction: discord.Interaction, code: str):
        code = code.upper()
        if code in self.stocks:
            del self.stocks[code]
            self.save_data()
            await interaction.response.send_message(f"📉 已成功下架股票公司 `{code}`。", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ 找不到股票代號為 `{code}` 的公司！", ephemeral=True)

    @app_commands.command(name="股票系統", description="檢視股市行情或調整漲跌")
    async def stock_market(self, interaction: discord.Interaction, code: str = None, change_percent: float = None):
        if not code:
            embed = discord.Embed(title="📊 當前股市行情", color=discord.Color.gold())
            for c, info in self.stocks.items():
                embed.add_field(name=f"{info['name']} (`{c}`)", value=f"目前股價: ${info['price']:.2f}", inline=False)
            await interaction.response.send_message(embed=embed)
            return

        code = code.upper()
        if code not in self.stocks:
            await interaction.response.send_message(f"❌ 找不到股票代號為 `{code}` 的公司！", ephemeral=True)
            return

        if change_percent is not None:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ 只有管理員可以調整股票漲跌幅！", ephemeral=True)
                return

            old_price = self.stocks[code]["price"]
            new_price = round(old_price * (1 + change_percent / 100), 2)
            self.stocks[code]["price"] = new_price
            self.save_data()

            status = "📈 上漲" if change_percent > 0 else "📉 下跌"
            await interaction.response.send_message(
                f"{status} **{self.stocks[code]['name']}** (`{code}`) 股價變動 {change_percent}%\n"
                f"原價格: ${old_price} -> **新價格: ${new_price}**"
            )
        else:
            info = self.stocks[code]
            await interaction.response.send_message(f"🏢 **{info['name']}** (`{code}`)\n目前股價: ${info['price']:.2f}")

async def setup(bot):
    await bot.add_cog(Stock(bot))
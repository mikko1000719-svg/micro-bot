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

    @app_commands.command(name="add_stock", description="Add a company to stock market")
    @app_commands.describe(code="Stock code (e.g., AAPL)", name="Company name", initial_price="Initial stock price")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_company(self, interaction: discord.Interaction, code: str, name: str, initial_price: float):
        code = code.upper()
        self.stocks[code] = {"name": name, "price": initial_price}
        self.save_data()
        await interaction.response.send_message(f"✅ Added `{code}` ({name}): ${initial_price}", ephemeral=True)

    @app_commands.command(name="remove_stock", description="Remove a company from stock market")
    @app_commands.describe(code="Stock code to remove")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_company(self, interaction: discord.Interaction, code: str):
        code = code.upper()
        if code in self.stocks:
            del self.stocks[code]
            self.save_data()
            await interaction.response.send_message(f"✅ Removed `{code}`", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Stock `{code}` not found", ephemeral=True)

    @app_commands.command(name="stock_market", description="View stock market")
    @app_commands.describe(code="Stock code (optional)", change_percent="Price change percentage (admin only)")
    async def stock_market(self, interaction: discord.Interaction, code: str = None, change_percent: float = None):
        if not code:
            embed = discord.Embed(title="📊 Stock Market", color=discord.Color.gold())
            for c, info in self.stocks.items():
                embed.add_field(name=f"{info['name']} (`{c}`)", value=f"Price: ${info['price']:.2f}", inline=False)
            await interaction.response.send_message(embed=embed)
            return

        code = code.upper()
        if code not in self.stocks:
            await interaction.response.send_message(f"❌ Stock `{code}` not found", ephemeral=True)
            return

        if change_percent is not None:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Administrator permission required", ephemeral=True)
                return

            old_price = self.stocks[code]["price"]
            new_price = round(old_price * (1 + change_percent / 100), 2)
            self.stocks[code]["price"] = new_price
            self.save_data()

            status = "📈 " if change_percent > 0 else "📉 "
            await interaction.response.send_message(
                f"{status} **{self.stocks[code]['name']}** (`{code}`) changed by {change_percent}%\n"
                f"Price: ${old_price} -> **Price: ${new_price}**"
            )
        else:
            info = self.stocks[code]
            await interaction.response.send_message(f"ℹ️ **{info['name']}** (`{code}`)\nPrice: ${info['price']:.2f}")

async def setup(bot):
    await bot.add_cog(Stock(bot))
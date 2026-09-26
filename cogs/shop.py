import os
import json
import discord
from discord import app_commands
from discord.ext import commands

DATA_FILE = "shop.json"

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shop_data = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"items": {}}

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.shop_data, f, indent=4)

    @app_commands.command(name="上架東西", description="上架新商品至商店")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_item(self, interaction: discord.Interaction, name: str, price: int, image_url: str = None):
        self.shop_data["items"][name] = {"price": price, "image": image_url}
        self.save_data()

        embed = discord.Embed(title="🛍️ 商品上架Success", description=f"**商品名稱**: {name}\n**價格**: ${price}", color=discord.Color.green())
        if image_url:
            embed.set_image(url=image_url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="購買東西", description="購買商店中的商品")
    async def buy_item(self, interaction: discord.Interaction, name: str):
        items = self.shop_data.get("items", {})
        if name not in items:
            await interaction.response.send_message(f"[ERROR] 找不到名為 `{name}` 的商品！", ephemeral=True)
            return

        item = items[name]
        embed = discord.Embed(title="🛒 購買Success", description=f"你Success購買了 **{name}**！\n扣除金額: ${item['price']}", color=discord.Color.blue())
        if item.get("image"):
            embed.set_thumbnail(url=item["image"])

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))
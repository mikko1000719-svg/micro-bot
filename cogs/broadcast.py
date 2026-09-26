import discord
from discord.ext import commands
from discord import app_commands

class Broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Save ID 
        self.opt_out_users = set()

    @app_commands.command(name="optout", description="[ 5.0] Bot")
    async def optout(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in self.opt_out_users:
            self.opt_out_users.remove(user_id)
            await interaction.response.send_message("[OK] **Cancel**，Receive。", ephemeral=True)
        else:
            self.opt_out_users.add(user_id)
            await interaction.response.send_message("🔕 Success****，ReceiveBot。", ephemeral=True)

    @app_commands.command(name="broadcast", description="[ 5.0] SendServer（Auto）")
    @app_commands.describe(message="")
    @app_commands.checks.has_permissions(administrator=True)
    async def broadcast(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        success_count = 0
        skip_count = 0

        embed = discord.Embed(
            title="[SPEAKER] 【Bot 5.0】",
            description=message,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Server：{guild.name}")

        for member in guild.members:
            if member.bot:
                continue
            if member.id in self.opt_out_users:
                skip_count += 1
                continue
            
            try:
                await member.send(embed=embed)
                success_count += 1
            except Exception:
                # Function
                skip_count += 1

        await interaction.followup.send(
            f"[OK] Send！\n- SuccessSend：**{success_count}**\n- /：**{skip_count}**", 
            ephemeral=True
        )

    @broadcast.error
    async def broadcast_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] Permission！ManageExecute。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Broadcast(bot))
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def notify_owner(self, guild: discord.Guild, user: discord.User, reason: str, channel: discord.TextChannel):
        """ Ticket """
        owner_cog = self.bot.get_cog("OwnerDM")
        if owner_cog and owner_cog.owner_id:
            try:
                owner = await self.bot.fetch_user(owner_cog.owner_id)
                if owner:
                    embed = discord.Embed(
                        title=" Error",
                        description=f"**Server**{guild.name}\n****{user.mention} (`{user.id}`)\n****{reason}\n**Channel**{channel.mention}",
                        color=discord.Color.gold()
                    )
                    await owner.send(embed=embed)
            except Exception as e:
                print(f"[TicketSystem]  Owner Failed: {e}")

    @app_commands.command(name="report", description="錯誤")
    async def report(self, interaction: discord.Interaction, reason: str):
        guild = interaction.guild
        user = interaction.user

        # SettingsChannelPermissionDefaultBot
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        # ManageManage
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel_name = f"ticket-{user.name}"
        ticket_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)

        embed = discord.Embed(
            title=" Error",
            description=f"****{user.mention}\n****{reason}\n\nProcessComplete `/close_ticket` Channel",
            color=discord.Color.orange()
        )
        await ticket_channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Channel{ticket_channel.mention}", ephemeral=True)

        # 
        await self.notify_owner(guild, user, reason, ticket_channel)

    @app_commands.command(name="close_ticket", description="頻道")
    async def close_ticket(self, interaction: discord.Interaction):
        if "ticket-" in interaction.channel.name:
            await interaction.response.send_message("🔒 Channel 5 Delete...")
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("❌ Command Ticket Channel", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))

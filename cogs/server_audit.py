import discord
from discord.ext import commands
from discord import app_commands

class ServerAudit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Channel IDChannel IDDictionary
        self.audit_channels = {}

    @app_commands.command(name="setupaudit", description="[ 5.0] AutoServerClassChannel")
    @app_commands.describe(category_id="ChannelClassCategoryID")
    @app_commands.checks.has_permissions(manage_channels=True, administrator=True)
    async def setupaudit(self, interaction: discord.Interaction, category_id: str):
        guild = interaction.guild
        
        try:
            cat_id = int(category_id)
            category = guild.get_channel(cat_id)
            if not isinstance(category, discord.CategoryChannel):
                await interaction.response.send_message("❌ ClassConfirmClass (Category)ID", ephemeral=True)
                return
        except ValueError:
            await interaction.response.send_message("❌ Class ID Number", ephemeral=True)
            return

        await interaction.response.send_message(" ServerChannelChannel...", ephemeral=True)

        # SettingsPermission@everyoneBotPermission
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }

        created_count = 0
        # ServerChannel
        for channel in guild.text_channels:
            # ClassChannel
            if channel.category_id == category.id:
                continue
                
            # ClassChannellog-
            log_channel_name = f"log-{channel.name}"
            
            try:
                log_channel = await guild.create_text_channel(
                    name=log_channel_name,
                    category=category,
                    overwrites=overwrites,
                    reason=f" 5.0 ChannelChannel: {channel.name}"
                )
                # 
                self.audit_channels[channel.id] = log_channel.id
                created_count += 1
            except Exception as e:
                print(f"Channel {log_channel_name} Failed: {e}")

        await interaction.followup.send(f"✅ CompleteSuccessClass `{category.name}`  **{created_count}** ChannelBot", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # BotMessageServerMessage
        if message.author.bot or not message.guild:
            return

        # CheckChannelMessageChannel
        log_channel_id = self.audit_channels.get(message.channel.id)
        if log_channel_id:
            log_channel = message.guild.get_channel(log_channel_id)
            if log_channel:
                # 
                content = (
                    f"📌 **Channel**{message.channel.mention}\n"
                    f" **Send**{message.author} (`{message.author.id}`)\n"
                    f" **Message**\n{message.content}"
                )
                
                # MessageGraph
                if message.attachments:
                    attachments_str = "\n".join([att.url for att in message.attachments])
                    content += f"\n ****\n{attachments_str}"

                try:
                    await log_channel.send(content)
                except Exception as e:
                    print(f"Failed: {e}")

    @setupaudit.error
    async def setupaudit_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            #  awa  it  await
            await interaction.response.send_message("❌ PermissionManageChannelManagePermissionExecuteCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerAudit(bot))
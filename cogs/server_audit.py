import discord
from discord.ext import commands
from discord import app_commands

class ServerAudit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 用來記錄「原始Channel ID」與「對應日誌Channel ID」的對照Dictionary
        self.audit_channels = {}

    @app_commands.command(name="setupaudit", description="[微國 5.0] Auto掃描Server並在指定Class中建立專屬日誌Channel")
    @app_commands.describe(category_id="請輸入要建立日誌Channel的Class（Category）ID")
    @app_commands.checks.has_permissions(manage_channels=True, administrator=True)
    async def setupaudit(self, interaction: discord.Interaction, category_id: str):
        guild = interaction.guild
        
        try:
            cat_id = int(category_id)
            category = guild.get_channel(cat_id)
            if not isinstance(category, discord.CategoryChannel):
                await interaction.response.send_message("[ERROR] 找不到該Class，請Confirm您輸入的是正確的「Class (Category)」ID！", ephemeral=True)
                return
        except ValueError:
            await interaction.response.send_message("[ERROR] Class ID 必須全部都是Number！", ephemeral=True)
            return

        await interaction.response.send_message("⚙️ 正在掃描ServerChannel並建立專屬日誌Channel，請稍候...", ephemeral=True)

        # SettingsPermission：所有人（@everyone）只能看、不能發言；Bot擁有完整Permission
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }

        created_count = 0
        # 掃描Server內所有的文字Channel
        for channel in guild.text_channels:
            # 略過已經在該日誌Class底下的Channel，避免重複迴圈
            if channel.category_id == category.id:
                continue
                
            # 在指定Class中建立對應的日誌Channel名稱（例如：log-一般聊天）
            log_channel_name = f"log-{channel.name}"
            
            try:
                log_channel = await guild.create_text_channel(
                    name=log_channel_name,
                    category=category,
                    overwrites=overwrites,
                    reason=f"微國 5.0 建立日誌Channel，對應原始Channel: {channel.name}"
                )
                # 建立對應對照
                self.audit_channels[channel.id] = log_channel.id
                created_count += 1
            except Exception as e:
                print(f"建立Channel {log_channel_name} Failed: {e}")

        await interaction.followup.send(f"[OK] 掃描與建立Complete！Success在Class `{category.name}` 中建立了 **{created_count}** 個專屬日誌Channel（僅限Bot發言）。", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 略過Bot自己的Message或非ServerMessage
        if message.author.bot or not message.guild:
            return

        # Check這個Channel的Message是否有對應的日誌Channel
        log_channel_id = self.audit_channels.get(message.channel.id)
        if log_channel_id:
            log_channel = message.guild.get_channel(log_channel_id)
            if log_channel:
                # 組合要複製過去的日誌內容
                content = (
                    f"[PIN] **來源Channel**：{message.channel.mention}\n"
                    f"👤 **Send者**：{message.author} (`{message.author.id}`)\n"
                    f"💬 **Message內容**：\n{message.content}"
                )
                
                # 如果Message包含Graph片或附件，一併附上網址
                if message.attachments:
                    attachments_str = "\n".join([att.url for att in message.attachments])
                    content += f"\n📎 **附件**：\n{attachments_str}"

                try:
                    await log_channel.send(content)
                except Exception as e:
                    print(f"轉發日誌Failed: {e}")

    @setupaudit.error
    async def setupaudit_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            # 這裡就是剛才出錯的地方，已經將 awa  it 修正為正確的 await
            await interaction.response.send_message("[ERROR] Permission不足！您需要「ManageChannel」與「Manage員」Permission才能Execute此Command。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerAudit(bot))
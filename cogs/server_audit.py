import discord
from discord.ext import commands
from discord import app_commands

class ServerAudit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 用來記錄「原始頻道 ID」與「對應日誌頻道 ID」的對照字典
        self.audit_channels = {}

    @app_commands.command(name="setupaudit", description="[微國 5.0] 自動掃描伺服器並在指定類別中建立專屬日誌頻道")
    @app_commands.describe(category_id="請輸入要建立日誌頻道的類別（Category）ID")
    @app_commands.checks.has_permissions(manage_channels=True, administrator=True)
    async def setupaudit(self, interaction: discord.Interaction, category_id: str):
        guild = interaction.guild
        
        try:
            cat_id = int(category_id)
            category = guild.get_channel(cat_id)
            if not isinstance(category, discord.CategoryChannel):
                await interaction.response.send_message("❌ 找不到該類別，請確認您輸入的是正確的「類別 (Category)」ID！", ephemeral=True)
                return
        except ValueError:
            await interaction.response.send_message("❌ 類別 ID 必須全部都是數字！", ephemeral=True)
            return

        await interaction.response.send_message("⚙️ 正在掃描伺服器頻道並建立專屬日誌頻道，請稍候...", ephemeral=True)

        # 設定權限：所有人（@everyone）只能看、不能發言；機器人擁有完整權限
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }

        created_count = 0
        # 掃描伺服器內所有的文字頻道
        for channel in guild.text_channels:
            # 略過已經在該日誌類別底下的頻道，避免重複迴圈
            if channel.category_id == category.id:
                continue
                
            # 在指定類別中建立對應的日誌頻道名稱（例如：log-一般聊天）
            log_channel_name = f"log-{channel.name}"
            
            try:
                log_channel = await guild.create_text_channel(
                    name=log_channel_name,
                    category=category,
                    overwrites=overwrites,
                    reason=f"微國 5.0 建立日誌頻道，對應原始頻道: {channel.name}"
                )
                # 建立對應對照
                self.audit_channels[channel.id] = log_channel.id
                created_count += 1
            except Exception as e:
                print(f"建立頻道 {log_channel_name} 失敗: {e}")

        await interaction.followup.send(f"✅ 掃描與建立完成！成功在類別 `{category.name}` 中建立了 **{created_count}** 個專屬日誌頻道（僅限機器人發言）。", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 略過機器人自己的訊息或非伺服器訊息
        if message.author.bot or not message.guild:
            return

        # 檢查這個頻道的訊息是否有對應的日誌頻道
        log_channel_id = self.audit_channels.get(message.channel.id)
        if log_channel_id:
            log_channel = message.guild.get_channel(log_channel_id)
            if log_channel:
                # 組合要複製過去的日誌內容
                content = (
                    f"📌 **來源頻道**：{message.channel.mention}\n"
                    f"👤 **發送者**：{message.author} (`{message.author.id}`)\n"
                    f"💬 **訊息內容**：\n{message.content}"
                )
                
                # 如果訊息包含圖片或附件，一併附上網址
                if message.attachments:
                    attachments_str = "\n".join([att.url for att in message.attachments])
                    content += f"\n📎 **附件**：\n{attachments_str}"

                try:
                    await log_channel.send(content)
                except Exception as e:
                    print(f"轉發日誌失敗: {e}")

    @setupaudit.error
    async def setupaudit_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            # 這裡就是剛才出錯的地方，已經將 awa  it 修正為正確的 await
            await interaction.response.send_message("❌ 權限不足！您需要「管理頻道」與「管理員」權限才能執行此指令。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerAudit(bot))
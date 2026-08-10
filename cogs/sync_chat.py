import discord
from discord.ext import commands
from discord import app_commands
import json
import os

DATA_FILE = "sync_data.json"

class SyncChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 結構: { 1: [channel_id1, channel_id2], 2: [...] }
        self.networks = self.load_data()
        self.msg_mapping = {}

    # --- JSON 資料存取區塊 ---
    def load_data(self):
        """讀取跨服群組資料，若檔案不存在則建立預設 1~10 空群組"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {int(k): set(v) for k, v in data.items()}
            except Exception as e:
                print(f"讀取 JSON 失敗: {e}")
        return {i: set() for i in range(1, 11)}

    def save_data(self):
        """將跨服群組資料安全地存入 JSON"""
        try:
            data = {str(k): list(v) for k, v in self.networks.items()}
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"儲存 JSON 失敗: {e}")

    # --- Webhook 取得機制 ---
    async def get_or_create_webhook(self, channel: discord.TextChannel):
        """尋找專用 Webhook，若無則自動建立"""
        webhooks = await channel.webhooks()
        for wh in webhooks:
            if wh.name == "WeiGuo_Sync_Webhook":
                return wh
        return await channel.create_webhook(name="WeiGuo_Sync_Webhook", reason="微國 5.0 跨服通訊專用 Webhook")

    # --- 跨服群組指令區塊 ---
    @app_commands.command(name="linkgroup", description="[微國 5.0] 將本頻道加入指定的跨服聯網群組 (1~10)")
    @app_commands.describe(group_id="請輸入群組編號 (1 到 10)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def linkgroup(self, interaction: discord.Interaction, group_id: int):
        if group_id < 1 or group_id > 10:
            await interaction.response.send_message("❌ 跨服群組編號必須介於 **1 到 10** 之間！", ephemeral=True)
            return

        if group_id not in self.networks:
            self.networks[group_id] = set()

        self.networks[group_id].add(interaction.channel_id)
        self.save_data() # 存檔
        
        await self.get_or_create_webhook(interaction.channel)

        embed = discord.Embed(
            title="🔗 跨服聯網群組加入成功",
            description=f"本頻道已成功連線至微國 5.0 **第 {group_id} 號跨服群組**！",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unlinkgroup", description="[微國 5.0] 將本頻道移出指定的跨服聯網群組")
    @app_commands.describe(group_id="請輸入要退出的群組編號 (1 到 10)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlinkgroup(self, interaction: discord.Interaction, group_id: int):
        if group_id in self.networks and interaction.channel_id in self.networks[group_id]:
            self.networks[group_id].remove(interaction.channel_id)
            self.save_data() # 更新存檔
            await interaction.response.send_message(f"🔌 已成功退出第 {group_id} 號跨服聯網群組。", ephemeral=True)
        else:
            await interaction.response.send_message("❌ 本頻道並未加入該跨服群組。", ephemeral=True)

    # --- 核心訊息同步區塊 ---
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # 判斷訊息發生在哪個跨服群組
        active_group = None
        for g_id, channels in self.networks.items():
            if message.channel.id in channels:
                active_group = g_id
                break

        if not active_group:
            return

        # 防呆機制：如果訊息沒有文字且沒有圖片，不處理
        if not message.content and not message.attachments:
            return

        # 處理藍色引述功能
        reply_prefix = ""
        if message.reference and message.reference.resolved:
            ref_msg = message.reference.resolved
            if isinstance(ref_msg, discord.Message) and ref_msg.content:
                reply_prefix = f"> 💬 回復 **{ref_msg.author.display_name}**: {ref_msg.content[:30]}...\n\n"

        full_content = reply_prefix + (message.content if message.content else "")

        target_tracker = {}
        for ch_id in self.networks[active_group]:
            if ch_id == message.channel.id:
                continue
            
            target_channel = self.bot.get_channel(ch_id)
            if target_channel and isinstance(target_channel, discord.TextChannel):
                try:
                    webhook = await self.get_or_create_webhook(target_channel)
                    
                    # 打包檔案
                    files = []
                    if message.attachments:
                        for att in message.attachments:
                            files.append(await att.to_file())

                    # 【修復重點】動態建立字典，只傳遞有效的變數，避開 NoneType 錯誤
                    send_kwargs = {
                        "username": f"{message.author.display_name} [{message.guild.name}]",
                        "avatar_url": message.author.display_avatar.url,
                        "wait": True
                    }
                    
                    # 只有在有文字時，才加入 content 參數
                    if full_content.strip():
                        send_kwargs["content"] = full_content
                        
                    # 只有在有檔案時，才加入 files 參數
                    if len(files) > 0:
                        send_kwargs["files"] = files

                    # 透過 ** 解包傳送
                    sent_msg = await webhook.send(**send_kwargs)
                    target_tracker[ch_id] = sent_msg
                except Exception as e:
                    print(f"Webhook 跨服發送失敗: {e}")

        if target_tracker:
            self.msg_mapping[message.id] = target_tracker

    # --- 表情符號復刻區塊 ---
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return

        msg_id = reaction.message.id
        if msg_id in self.msg_mapping:
            for ch_id, sent_msg in self.msg_mapping[msg_id].items():
                try:
                    await sent_msg.add_reaction(reaction.emoji)
                except Exception as e:
                    print(f"跨服反應復刻失敗: {e}")

async def setup(bot):
    await bot.add_cog(SyncChat(bot))
import os
import json
import asyncio
import discord
from discord.ext import commands

CONFIG_FILE = "bot_owner.json"

class OwnerDM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = self.load_owner_id()
        self.latest_error = "✅ SystemError" # SystemError

    def load_owner_id(self):
        """ JSON FileLoad ID"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("owner_id")
            except Exception as e:
                print(f"[Bot 5.0] Read Owner ConfigurationFailed: {e}")
        return None

    def save_owner_id(self, user_id: int):
        """ ID Save JSON File"""
        self.owner_id = user_id
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"owner_id": user_id}, f, ensure_ascii=False, indent=4)
            print(f"[Bot 5.0] Success ID: {user_id}")
        except Exception as e:
            print(f"[Bot 5.0] Save Owner ConfigurationFailed: {e}")

    def log_error(self, error_msg: str):
        """Error"""
        self.latest_error = f"🛑 Error: {error_msg}"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # BotMessage
        if message.author.bot:
            return

        # Process (DMChannel)
        if isinstance(message.channel, discord.DMChannel):
            user_id = message.author.id

            # SettingsSettings
            if self.owner_id is None:
                self.save_owner_id(user_id)
                await message.channel.send(f" VerifySuccess **Bot 5.0** ")
                return

            # Send
            if user_id != self.owner_id:
                await message.channel.send("❌ Bot 5.0 ")
                return

            # === SystemServerList ===
            await message.channel.send("[SWITCH] ReadServer...")

            embed = discord.Embed(
                title="🛡️ Bot 5.0 - ",
                description=f"**System**{self.latest_error}\n**Connection (Ping)**`{round(self.bot.latency * 1000)} ms`\n**Server**`{len(self.bot.guilds)}` ",
                color=discord.Color.blue()
            )

            guild_info_list = []
            for guild in self.bot.guilds:
                invite_url = ""
                
                # SendChannel API Rate Limit (429)
                try:
                    for channel in guild.text_channels:
                        if channel.permissions_for(guild.me).create_instant_invite:
                            invite = await channel.create_invite(max_age=3600, max_uses=5, reason="Bot")
                            invite_url = invite.url
                            break
                except Exception:
                    pass

                guild_info_list.append(f"• **{guild.name}** (ID: `{guild.id}`)\n  : {guild.member_count} | [Server]({invite_url})")
                
                # Defense API  429 Error
                await asyncio.sleep(0.2)

            # Process Discord Message 4000 Limit
            guild_chunks = [guild_info_list[i:i + 5] for i in range(0, len(guild_info_list), 5)]
            
            for index, chunk in enumerate(guild_chunks):
                field_title = " ServerList" if index == 0 else f" ServerList ( {index + 1})"
                embed.add_field(name=field_title, value="\n".join(chunk), inline=False)

            await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(OwnerDM(bot))

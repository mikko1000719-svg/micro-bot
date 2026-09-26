# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord import app_commands
import json
import os

DATA_FILE = "sync_data.json"

class SyncChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Structure: { 1: [channel_id1, channel_id2], 2: [...] }
        self.networks = self.load_data()
        self.msg_mapping = {}

    # --- JSON data access block ---
    def load_data(self):
        """Read cross-server group data, create default 1-10 empty groups if file doesn't exist"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {int(k): set(v) for k, v in data.items()}
            except Exception as e:
                print(f"Failed to read JSON: {e}")
        return {i: set() for i in range(1, 11)}

    def save_data(self):
        """Safely save cross-server group data to JSON"""
        try:
            data = {str(k): list(v) for k, v in self.networks.items()}
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Failed to save JSON: {e}")

    # --- Webhook acquisition mechanism ---
    async def get_or_create_webhook(self, channel: discord.TextChannel):
        """Find dedicated Webhook, create automatically if not exists"""
        webhooks = await channel.webhooks()
        for wh in webhooks:
            if wh.name == "WeiGuo_Sync_Webhook":
                return wh
        return await channel.create_webhook(name="WeiGuo_Sync_Webhook", reason="WeiGuo 5.0 cross-server communication dedicated Webhook")

    # --- Cross-server group command block ---
    @app_commands.command(name="linkgroup", description="[WeiGuo 5.0] Add this channel to specified cross-server network group (1~10)")
    @app_commands.describe(group_id="Please enter group number (1 to 10)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def linkgroup(self, interaction: discord.Interaction, group_id: int):
        if group_id < 1 or group_id > 10:
            await interaction.response.send_message("[ERROR] Cross-server group number must be between **1 to 10**!", ephemeral=True)
            return

        if group_id not in self.networks:
            self.networks[group_id] = set()

        self.networks[group_id].add(interaction.channel_id)
        self.save_data() # Save

        await self.get_or_create_webhook(interaction.channel)

        embed = discord.Embed(
            title="[LINK] Cross-server network group join successful",
            description=f"This channel has successfully connected to WeiGuo 5.0 **Group {group_id} cross-server group**!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unlinkgroup", description="[WeiGuo 5.0] Remove this channel from specified cross-server network group")
    @app_commands.describe(group_id="Please enter the group number to exit (1 to 10)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlinkgroup(self, interaction: discord.Interaction, group_id: int):
        if group_id in self.networks and interaction.channel_id in self.networks[group_id]:
            self.networks[group_id].remove(interaction.channel_id)
            self.save_data() # Update save
            await interaction.response.send_message(f"[UNLINK] Successfully exited Group {group_id} cross-server network group.", ephemeral=True)
        else:
            await interaction.response.send_message("[ERROR] This channel is not in that cross-server group.", ephemeral=True)

    # --- Core message synchronization block ---
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # Determine which cross-server group the message occurred in
        active_group = None
        for g_id, channels in self.networks.items():
            if message.channel.id in channels:
                active_group = g_id
                break

        if not active_group:
            return

        # Fool-proof mechanism: if message has no text and no images, don't process
        if not message.content and not message.attachments:
            return

        # Handle blue quote function
        reply_prefix = ""
        if message.reference and message.reference.resolved:
            ref_msg = message.reference.resolved
            if isinstance(ref_msg, discord.Message) and ref_msg.content:
                reply_prefix = f">  Reply to **{ref_msg.author.display_name}**: {ref_msg.content[:30]}...\n\n"

        full_content = reply_prefix + (message.content if message.content else "")

        target_tracker = {}
        for ch_id in self.networks[active_group]:
            if ch_id == message.channel.id:
                continue

            target_channel = self.bot.get_channel(ch_id)
            if target_channel and isinstance(target_channel, discord.TextChannel):
                try:
                    webhook = await self.get_or_create_webhook(target_channel)

                    # Package files
                    files = []
                    if message.attachments:
                        for att in message.attachments:
                            files.append(await att.to_file())

                    # [Fix key point] Dynamically build dictionary, only pass valid variables, avoid NoneType error
                    send_kwargs = {
                        "username": f"{message.author.display_name} [{message.guild.name}]",
                        "avatar_url": message.author.display_avatar.url,
                        "wait": True
                    }

                    # Only add content parameter if there is text
                    if full_content.strip():
                        send_kwargs["content"] = full_content

                    # Only add files parameter if there are files
                    if len(files) > 0:
                        send_kwargs["files"] = files

                    # Send via ** unpacking
                    sent_msg = await webhook.send(**send_kwargs)
                    target_tracker[ch_id] = sent_msg
                except Exception as e:
                    print(f"Webhook cross-server send failed: {e}")

        if target_tracker:
            self.msg_mapping[message.id] = target_tracker

    # --- Emoji reaction replication block ---
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
                    print(f"Cross-server reaction replication failed: {e}")

async def setup(bot):
    await bot.add_cog(SyncChat(bot))
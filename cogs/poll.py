import discord
from discord import app_commands
from discord.ext import commands

class PollReasonModal(discord.ui.Modal, title="請填寫投票原因"):
    reason_input = discord.ui.TextInput(
        label="投票原因（選填）",
        style=discord.TextStyle.paragraph,
        placeholder="請在此輸入您投下此票的原因...",
        required=False,
        max_length=300
    )

    def __init__(self, vote_type: str, view_instance):
        super().__init__()
        self.vote_type = vote_type
        self.view_instance = view_instance

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        reason = self.reason_input.value if self.reason_input.value else "未提供原因"

        # 記錄或更新使用者的投票與原因
        self.view_instance.user_votes[user_id] = {
            "choice": self.vote_type,
            "reason": reason,
            "name": interaction.user.name
        }

        # 重新計算各選項票數
        self.view_instance.calculate_votes()
        await self.view_instance.update_poll_message(interaction)

class PollView(discord.ui.View):
    def __init__(self, question: str):
        super().__init__(timeout=86400)  # 24小時超時
        self.question = question
        # 記錄每個使用者的投票資料 {user_id: {"choice": "同意/不同意/棄權", "reason": "原因", "name": "名字"}}
        self.user_votes = {}
        self.agree_count = 0
        self.disagree_count = 0
        self.abstain_count = 0

    def calculate_votes(self):
        self.agree_count = sum(1 for data in self.user_votes.values() if data["choice"] == "同意")
        self.disagree_count = sum(1 for data in self.user_votes.values() if data["choice"] == "不同意")
        self.abstain_count = sum(1 for data in self.user_votes.values() if data["choice"] == "棄權")

    @discord.ui.button(label="同意", style=discord.ButtonStyle.green, custom_id="poll_agree")
    async def vote_agree(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PollReasonModal("同意", self))

    @discord.ui.button(label="不同意", style=discord.ButtonStyle.red, custom_id="poll_disagree")
    async def vote_disagree(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PollReasonModal("不同意", self))

    @discord.ui.button(label="棄權", style=discord.ButtonStyle.grey, custom_id="poll_abstain")
    async def vote_abstain(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PollReasonModal("棄權", self))

    async def update_poll_message(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📊 伺服器正式投票",
            description=f"**問題：** {self.question}",
            color=discord.Color.blue()
        )
        total_votes = len(self.user_votes)
        
        embed.add_field(name=f"🟢 同意", value=f"**{self.agree_count}** 票", inline=True)
        embed.add_field(name=f"🔴 不同意", value=f"**{self.disagree_count}** 票", inline=True)
        embed.add_field(name=f"🟡 棄權", value=f"**{self.abstain_count}** 票", inline=True)

        # 整理最近幾位投票者的原因清單顯示在下方
        if self.user_votes:
            reasons_text = "\n".join([f"• **{data['name']}** ({data['choice']})：{data['reason']}" for data in list(self.user_votes.values())[-5:]])
            embed.add_field(name="💬 最近投票與原因紀錄", value=reasons_text, inline=False)

        embed.set_footer(text=f"總投票人數：{total_votes} 人 (再次點擊按鈕可修改您的投票與原因)")

        await interaction.response.edit_message(embed=embed, view=self)

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="發起一個包含同意、不同意、棄權及原因填寫的投票")
    @app_commands.describe(question="投票主題/問題")
    async def poll(self, interaction: discord.Interaction, question: str):
        view = PollView(question=question)
        
        embed = discord.Embed(
            title="📊 伺服器正式投票",
            description=f"**問題：** {question}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🟢 同意", value="**0** 票", inline=True)
        embed.add_field(name="🔴 不同意", value="**0** 票", inline=True)
        embed.add_field(name="🟡 棄權", value="**0** 票", inline=True)
        embed.set_footer(text=f"發起人：{interaction.user.name} | 總投票人數：0 人")

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Poll(bot))
    
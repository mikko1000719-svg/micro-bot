import discord
from discord import app_commands
from discord.ext import commands

class PollReasonModal(discord.ui.Modal, title=""):
    reason_input = discord.ui.TextInput(
        label="（）",
        style=discord.TextStyle.paragraph,
        placeholder="...",
        required=False,
        max_length=300
    )

    def __init__(self, vote_type: str, view_instance):
        super().__init__()
        self.vote_type = vote_type
        self.view_instance = view_instance

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        reason = self.reason_input.value if self.reason_input.value else ""

        # Update
        self.view_instance.user_votes[user_id] = {
            "choice": self.vote_type,
            "reason": reason,
            "name": interaction.user.name
        }

        # Re-Option
        self.view_instance.calculate_votes()
        await self.view_instance.update_poll_message(interaction)

class PollView(discord.ui.View):
    def __init__(self, question: str):
        super().__init__(timeout=86400)  # 24
        self.question = question
        #  {user_id: {"choice": "//", "reason": "", "name": ""}}
        self.user_votes = {}
        self.agree_count = 0
        self.disagree_count = 0
        self.abstain_count = 0

    def calculate_votes(self):
        self.agree_count = sum(1 for data in self.user_votes.values() if data["choice"] == "")
        self.disagree_count = sum(1 for data in self.user_votes.values() if data["choice"] == "")
        self.abstain_count = sum(1 for data in self.user_votes.values() if data["choice"] == "")

    @discord.ui.button(label="", style=discord.ButtonStyle.green, custom_id="poll_agree")
    async def vote_agree(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PollReasonModal("", self))

    @discord.ui.button(label="", style=discord.ButtonStyle.red, custom_id="poll_disagree")
    async def vote_disagree(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PollReasonModal("", self))

    @discord.ui.button(label="", style=discord.ButtonStyle.grey, custom_id="poll_abstain")
    async def vote_abstain(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PollReasonModal("", self))

    async def update_poll_message(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="[STAT] Server",
            description=f"**：** {self.question}",
            color=discord.Color.blue()
        )
        total_votes = len(self.user_votes)
        
        embed.add_field(name=f"[OK] ", value=f"**{self.agree_count}** ", inline=True)
        embed.add_field(name=f"[STOP] ", value=f"**{self.disagree_count}** ", inline=True)
        embed.add_field(name=f"[WAIT] ", value=f"**{self.abstain_count}** ", inline=True)

        # Display
        if self.user_votes:
            reasons_text = "\n".join([f"• **{data['name']}** ({data['choice']})：{data['reason']}" for data in list(self.user_votes.values())[-5:]])
            embed.add_field(name="💬 ", value=reasons_text, inline=False)

        embed.set_footer(text=f"：{total_votes}  ()")

        await interaction.response.edit_message(embed=embed, view=self)

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="、、")
    @app_commands.describe(question="/")
    async def poll(self, interaction: discord.Interaction, question: str):
        view = PollView(question=question)
        
        embed = discord.Embed(
            title="[STAT] Server",
            description=f"**：** {question}",
            color=discord.Color.blue()
        )
        embed.add_field(name="[OK] ", value="**0** ", inline=True)
        embed.add_field(name="[STOP] ", value="**0** ", inline=True)
        embed.add_field(name="[WAIT] ", value="**0** ", inline=True)
        embed.set_footer(text=f"：{interaction.user.name} | ：0 ")

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Poll(bot))
    
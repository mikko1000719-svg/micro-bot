import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio

# 優化 yt-dlp 設定，增加提取速度與防錯
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'extract_flat': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # 綁定 IPv4 避免部分網路連線卡住
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play", description="播放 YouTube 音樂")
    @app_commands.describe(url="YouTube 音樂網址")
    async def play(self, interaction: discord.Interaction, url: str):
        if not interaction.user.voice:
            await interaction.response.send_message("指揮官，你必須先進入一個語音頻道才能使用此指令！", ephemeral=True)
            return

        await interaction.response.defer()
        channel = interaction.user.voice.channel

        try:
            if interaction.guild.voice_client is None:
                voice_client = await channel.connect()
            else:
                voice_client = interaction.guild.voice_client
                await voice_client.move_to(channel)

            # 非同步抓取音樂資訊，並加上錯誤處理
            loop = asyncio.get_running_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            
            if 'entries' in data:
                # 抓取播放清單的第一首歌
                data = data['entries'][0]

            audio_url = data.get('url')
            title = data.get('title', '未知標題')
            
            ffmpeg_executable = r"C:\Users\User\Downloads\ffmpeg-9.0-essentials_build\ffmpeg-9.0-essentials_build\bin\ffmpeg.exe"
            ffmpeg_options = {'options': '-vn'}
            
            player = discord.FFmpegPCMAudio(audio_url, executable=ffmpeg_executable, **ffmpeg_options)
            
            if voice_client.is_playing():
                voice_client.stop()

            voice_client.play(player)
            await interaction.followup.send(f"🎶 正在為您播放：**{title}**")
        
        except Exception as e:
            # 將詳細錯誤印在你的 VS Code 終端機裡，方便我們查看
            print(f"音樂播放發生嚴重錯誤: {e}")
            await interaction.followup.send(f"播放失敗，無法順利取得音樂串流。請檢查網址或稍後再試！", ephemeral=True)

    @app_commands.command(name="stop", description="停止音樂並讓機器人退出語音頻道")
    async def stop(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("已停止音樂，機器人已退出語音頻道。", ephemeral=True)
        else:
            await interaction.response.send_message("機器人目前不在任何語音頻道中。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Music(bot))
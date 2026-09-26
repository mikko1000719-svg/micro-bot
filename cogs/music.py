import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 建立一個字典來管理不同伺服器 (Guild) 的播放佇列
        self.music_queue = {}

    # --- 工具函式 1：解析搜尋結果或歌單 ---
    def fetch_soundcloud_info(self, query: str):
        is_url = query.startswith("http://") or query.startswith("https://")
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': is_url  # 歌單只抓目錄，加快速度
        }
        search_query = query if is_url else f"scsearch1:{query}"

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    # 為了簡單起見，如果是歌單，我們先抓第一首示範 (你可以後續擴充為加入多首)
                    return info['entries'][0]
                elif not 'entries' in info:
                    return info
                return None
        except Exception as e:
            print(f"解析錯誤: {e}")
            return None

    # --- 工具函式 2：取得真實的音訊串流連結 ---
    def get_stream_url(self, web_url: str):
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(web_url, download=False)
                return info['url']
        except Exception:
            return None

    # --- 核心邏輯：播放下一首歌 ---
    def play_next(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        voice_client = interaction.guild.voice_client

        # 檢查佇列中是否還有歌曲
        if guild_id in self.music_queue and len(self.music_queue[guild_id]) > 0:
            # 拿出佇列中的第一首歌
            next_song = self.music_queue[guild_id].pop(0)
            
            # 解析真實的串流網址
            stream_url = self.get_stream_url(next_song['url'])
            
            if stream_url and voice_client:
                # 設定 FFmpeg 參數，這能讓網路串流更穩定，避免斷音
                ffmpeg_options = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn' # -vn 代表不需要影片，只要音訊
                }
                
                # 播放音訊！播完後自動呼叫自己 (play_next) 播下一首
                voice_client.play(
                    discord.FFmpegPCMAudio(stream_url, **ffmpeg_options),
                    after=lambda e: self.play_next(interaction)
                )
        else:
            # 如果歌單播完了，我們可以讓機器人離開語音頻道 (可選)
            # asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.bot.loop)
            pass

    # --- 斜線指令：/play ---
    @app_commands.command(name="play", description="在 SoundCloud 搜尋並播放音樂")
    @app_commands.describe(query="請輸入歌曲名稱或 SoundCloud 網址")
    async def play(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()

        # 1. 檢查使用者狀態
        if not interaction.user.voice:
            await interaction.followup.send("[ERROR] 你必須先加入一個語音頻道！")
            return

        # 2. 機器人加入語音頻道
        voice_channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client

        if not voice_client:
            # 如果機器人還沒在頻道裡，就連線進去
            await voice_channel.connect()
            voice_client = interaction.guild.voice_client
        elif voice_client.channel != voice_channel:
            # 如果機器人在別的頻道，就移動過來
            await voice_client.move_to(voice_channel)

        # 3. 搜尋歌曲
        loop = asyncio.get_event_loop()
        track_info = await loop.run_in_executor(None, self.fetch_soundcloud_info, query)

        # 4. 加入佇列與播放邏輯
        if track_info:
            guild_id = interaction.guild.id
            
            # 如果這個伺服器還沒有佇列，就幫它建立一個空的 List
            if guild_id not in self.music_queue:
                self.music_queue[guild_id] = []
                
            # 把歌曲加入佇列
            self.music_queue[guild_id].append(track_info)
            
            title = track_info.get('title', '未知歌曲')
            await interaction.followup.send(f"[MUSIC] 已加入佇列：**{title}**")

            # 如果機器人目前「沒有」在播放音樂，我們就主動觸發播放
            if not voice_client.is_playing():
                self.play_next(interaction)
        else:
            await interaction.followup.send(f"[ERROR] 找不到與「{query}」相關的歌曲。")

async def setup(bot):
    await bot.add_cog(Music(bot))

import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # DictionaryManageServer (Guild) Queue
        self.music_queue = {}

    # ---  1Search ---
    def fetch_soundcloud_info(self, query: str):
        is_url = query.startswith("http://") or query.startswith("https://")
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': is_url  # 
        }
        search_query = query if is_url else f"scsearch1:{query}"

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    #  ()
                    return info['entries'][0]
                elif not 'entries' in info:
                    return info
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    # ---  2 ---
    def get_stream_url(self, web_url: str):
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(web_url, download=False)
                return info['url']
        except Exception:
            return None

    # ---  ---
    def play_next(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        voice_client = interaction.guild.voice_client

        # CheckQueue
        if guild_id in self.music_queue and len(self.music_queue[guild_id]) > 0:
            # Queue
            next_song = self.music_queue[guild_id].pop(0)
            
            # 
            stream_url = self.get_stream_url(next_song['url'])
            
            if stream_url and voice_client:
                # Settings FFmpeg ParameterNetwork
                ffmpeg_options = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn' # -vn 
                }
                
                # Auto (play_next) 
                voice_client.play(
                    discord.FFmpegPCMAudio(stream_url, **ffmpeg_options),
                    after=lambda e: self.play_next(interaction)
                )
        else:
            # BotChannel ()
            # asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.bot.loop)
            pass

    # --- Command/play ---
    @app_commands.command(name="play", description=" SoundCloud Search")
    @app_commands.describe(query=" SoundCloud ")
    async def play(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()

        # 1. Check
        if not interaction.user.voice:
            await interaction.followup.send("❌ Channel")
            return

        # 2. BotChannel
        voice_channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client

        if not voice_client:
            # BotChannelConnection
            await voice_channel.connect()
            voice_client = interaction.guild.voice_client
        elif voice_client.channel != voice_channel:
            # BotChannel
            await voice_client.move_to(voice_channel)

        # 3. Search
        loop = asyncio.get_event_loop()
        track_info = await loop.run_in_executor(None, self.fetch_soundcloud_info, query)

        # 4. Queue
        if track_info:
            guild_id = interaction.guild.id
            
            # ServerQueue List
            if guild_id not in self.music_queue:
                self.music_queue[guild_id] = []
                
            # Queue
            self.music_queue[guild_id].append(track_info)
            
            title = track_info.get('title', '')
            await interaction.followup.send(f"🎵 Queue**{title}**")

            # Bot
            if not voice_client.is_playing():
                self.play_next(interaction)
        else:
            await interaction.followup.send(f"❌ {query}")

async def setup(bot):
    await bot.add_cog(Music(bot))

import nextcord
from nextcord.ext import commands
from __main__ import EMBED_COLOR
import os
from ..libs.oclib import *

PREFIX = os.getenv("PREFIX")


class PingResponse(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.stars = 0
        self.forks = 0
        self.bot.loop.create_task(self.fetch_repo_data())

    async def fetch_repo_data(self):
        try:
            repo_data = await request("https://api.github.com/repos/orxngc/takina")
            if not repo_data:
                return
            self.stars = repo_data.get("stargazers_count", 0)
            self.forks = repo_data.get("forks_count", 0)
        except Exception as e:
            print(f"Error fetching repository data: {e}")

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if self.bot.user.mentioned_in(message) and not message.author.bot:
            if message.content.strip() == message.guild.me.mention:
                embed = nextcord.Embed(
                    title="Takina",
                    url="https://github.com/orxngc/takina",
                    description="Takina is a multipurpose opensource bot written in Python. More information is available in the [Github repository](https://github.com/orxngc/takina).",
                    color=EMBED_COLOR,
                )
                uptime = await uptime_fetcher()
                embed.add_field(name="Prefix", value=PREFIX, inline=True)
                embed.add_field(name="Stars", value=str(self.stars), inline=True)
                embed.add_field(name="Uptime", value=uptime, inline=True)
                embed.set_author(name="orangc", url="https://orangc.xyz", icon_url="https://cdn.discordapp.com/avatars/961063229168164864/4bfbf378514a9dcc7a619b5ce5e7e57c.webp")
                await message.reply(embed=embed, mention_author=False)

def setup(bot: commands.Bot):
    bot.add_cog(PingResponse(bot))

import nextcord
from nextcord.ext import commands
from config import *
from ..libs.oclib import *
from wynn_api import (
    getPlayer as get_player,
    getPlayerCharacter as get_character,
    getPlayerCharacterList as get_character_list,
    getGuild as get_guild,
    getItemMetadata as get_item,
)
from datetime import datetime


def parse_iso8601(date_str):
    formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Date string '{date_str}' is not in a recognized format.")
    return dt.strftime("%B %-d, %Y at %-H.%M")


class WynnPlayers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def player_information_embed_builder(self, player):
        embed = nextcord.Embed(color=EMBED_COLOR)
        embed.description = ""

        if player.get("Error"):
            error_embed = nextcord.Embed(color=ERROR_COLOR)
            error_embed.description = ":x: No player found with that username."
            return error_embed

        username = player.get("username")
        uuid = player.get("uuid")
        rank = player.get("rank")
        server = player.get("server")
        online = player.get("online")
        playtime = player.get("playtime")
        join_date = player.get("firstJoin")
        last_join = player.get("lastJoin")
        guild = player.get("guild")
        veteran = player.get("veteran")
        forum = player.get("forumLink")
        gd = player.get("globalData")
        wars = gd.get("wars")
        total_level = gd.get("totalLevels")
        dungeons = gd.get("dungeons").get("total")
        raids = gd.get("raids").get("total")
        quests = gd.get("completedQuests")
        pvp_kills = gd.get("pvp").get("kills")
        pvp_deaths = gd.get("pvp").get("deaths")
        mobs = gd.get("killedMobs")
        chests = gd.get("chestsFound")

        embed.url = f"https://wynncraft.com/stats/player/{uuid}"
        embed.title = username
        embed.set_thumbnail(f"https://visage.surgeplay.com/bust/256/{uuid}.webp")

        if online:
            embed.description += f"-# Currently online on {server}."
        else:
            last_join = parse_iso8601(last_join)
            embed.description += f"-# Last seen {last_join}"

        if guild:
            guild_name = guild.get("name")
            guild_prefix = guild.get("prefix")
            guild_rank = guild.get("rank")
            guild = (
                f"{guild_rank.lower().capitalize()} of [{guild_prefix}] {guild_name}"
            )
            embed.description += f"\n\n> **Guild**: {guild}"

        if rank != "Player":
            embed.description += f"\n> **Rank**: {rank}"

        embed.description += f"\n> **Playtime**: {playtime} hours"

        join_date = parse_iso8601(join_date)
        embed.description += f"\n> **Joined**: {join_date}"

        embed.description += f"\n> **Mobs killed**: {mobs}"
        embed.description += f"\n> **Chests opened**: {chests}"
        embed.description += f"\n> **Quests completed**: {quests}"
        embed.description += f"\n> **Dungeons completed**: {dungeons}"
        embed.description += f"\n> **Total level**: {total_level}"

        if raids > 0:
            embed.description += f"\n> **Raids**: {raids}"
        if wars > 0:
            embed.description += f"\n> **Wars**: {wars}"

        if forum:
            embed.description += f"\n> **Forum account**: [Linked](https://forums.wynncraft.com/members/{forum}/)"

        if pvp_deaths and pvp_kills:
            embed.description += f"\n> **PVP**: {pvp_kills} kills / {pvp_deaths} deaths"

        return embed

    @commands.group(
        name="wynn",
        aliases=["wynncraft"],
        description="Base wynncraft command, if no subcommand is passed.",
        invoke_without_command=True,
    )
    async def wynn(self, ctx: commands.Context):
        embed = nextcord.Embed(
            description=":x: Please specify a subcommand: `player`, `guild`, or `item`",
            color=ERROR_COLOR,
        )
        await ctx.reply(embed=embed, mention_author=False)

    @wynn.command(
        name="player",
        help="Fetch and display a Wynncraft player's data. Usage: `wynn player <minecraft username>`.",
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def player(self, ctx: commands.Context, username: str):
        player = get_player(username)
        embed = await self.player_information_embed_builder(player)
        await ctx.reply(embed=embed, mention_author=False)
    
    @nextcord.slash_command(name="wynn", description="Wynncraft utility commands.")
    async def slash_wynn(self, interaction: nextcord.Interaction):
        pass
    
    @slash_wynn.subcommand(name="player", description="Fetch and display a Wynncraft player's data.")
    async def slash_player(
        self,
        interaction: nextcord.Interaction,
        username: str = nextcord.SlashOption(
            description="The player to fetch information on", required=True
        )
    ):
        player = get_player(username)
        embed = await self.player_information_embed_builder(player)
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(WynnPlayers(bot))

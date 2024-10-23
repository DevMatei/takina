import os
import nextcord
from nextcord.ext import commands, application_checks
from motor.motor_asyncio import AsyncIOMotorClient
from __main__ import DB_NAME, EMBED_COLOR


class Prefix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = AsyncIOMotorClient(os.getenv("MONGO")).get_database(DB_NAME)

    @nextcord.slash_command(name="prefix", description="Set a custom prefix for Takina")
    @application_checks.has_permissions(administrator=True)
    async def set_prefix(self, interaction: nextcord.Interaction, new_prefix: str):
        guild_id = interaction.guild.id

        await self.db.prefixes.update_one(
            {"guild_id": guild_id}, {"$set": {"prefix": new_prefix}}, upsert=True
        )
        embed = nextcord.Embed(color=EMBED_COLOR)
        embed.description = f"✅ Prefix updated to: `{new_prefix}`"
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Prefix(bot))

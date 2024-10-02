import re
from nextcord.ext import commands
import nextcord
from nextcord import SlashOption
from __main__ import BOT_NAME, EMBED_COLOR
from ..libs.oclib import *


class ModUtils(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.has_permissions(moderate_members=True, manage_messages=True)
    async def send(
        self,
        ctx: commands.Context,
        channel: nextcord.TextChannel = None,
        *,
        message: str,
    ):
        """Send a message as the bot. Usage: `send channel message`."""
        if channel and message:
            await channel.send(message)
            await ctx.reply("Successfully sent message.", mention_author=False)
        elif message:
            await ctx.reply(message, mention_author=False)
        else:
            await ctx.reply(
                "Please provide a message and channel to use this command.",
                mention_author=False,
            )

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int):
        """Purges a specified number of messages. Usage: `purge number`, where number is the number of messages you would like to purge."""

        # Ensure the number is a positive integer
        if amount <= 0:
            await ctx.reply(
                "Please specify a positive number of messages to purge.",
                mention_author=False,
            )
            return

        deleted = await ctx.channel.purge(limit=amount)
        await ctx.reply(
            f"Successfully purged {len(deleted)} messages.",
            delete_after=3,
            mention_author=False,
        )

    @commands.command(aliases=["setnick"])
    @commands.has_permissions(manage_nicknames=True)
    async def nick(
        self, ctx: commands.Context, member: str = None, *, nickname: str = None
    ):
        """Change a members nickname. Usage: `setnick member new_nickname`."""
        if member is None:
            member = ctx.author
        else:
            member = extract_user_id(member, ctx)

        # Check permissions
        can_proceed, message = perms_check(member, ctx, author_check=False)
        if not can_proceed:
            await ctx.reply(message, mention_author=False)
            return

        if not nickname:
            nickname = member.name

        await member.edit(nick=nickname)
        await ctx.reply(
            f"**{member.name}**'s nickname has been changed to **{nickname}**.",
            mention_author=False,
        )


class ModUtilsSlash(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @nextcord.slash_command(name="send")
    @application_checks.has_permissions(moderate_members=True, manage_messages=True)
    async def slash_send(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel = SlashOption(
            description="The channel to send the message in", required=True
        ),
        *,
        message: str = SlashOption(description="The message to send", required=True),
    ):
        """Send a message as the bot."""
        if channel and message:
            await channel.send(message)
            await interaction.send("Successfully sent message.", ephemeral=True)
        elif message:
            await interaction.send(message, ephemeral=True)
        else:
            await interaction.send(
                "Please provide a message and channel to use this command.",
                ephemeral=True,
            )

    @nextcord.slash_command(
        name="purge", description="Purges a specified number of messages."
    )
    @application_checks.has_permissions(manage_messages=True)
    async def slash_purge(
        self,
        interaction: nextcord.Interaction,
        amount: int = SlashOption(
            description="Number of messages to purge", required=True
        ),
    ):
        """Purges a specified number of messages."""
        if amount <= 0:
            await interaction.send(
                "Please specify a positive number of messages to purge.", ephemeral=True
            )
            return

        deleted = await interaction.channel.purge(limit=amount)
        await interaction.send(
            f"Successfully purged {len(deleted)} messages.", ephemeral=True
        )

    @nextcord.slash_command(name="nick", description="Change a member's nickname.")
    @application_checks.has_permissions(manage_nicknames=True)
    async def slash_nick(
        self,
        interaction: nextcord.Interaction,
        member: str = SlashOption(
            description="Member to change the nickname for", required=True
        ),
        nickname: str = SlashOption(description="New nickname"),
    ):
        """Change a member's nickname."""
        if member is None:
            member = ctx.author
        else:
            member = extract_user_id(member, ctx)

        # Check permissions
        can_proceed, message = perms_check(member, ctx, author_check=False)
        if not can_proceed:
            await interaction.send(message, ephemeral=True)
            return

        if not nickname:
            nickname = member.name

        await member.edit(nick=nickname)
        await interaction.send(
            f"**{member.name}**'s nickname has been changed to **{nickname}**.",
            ephemeral=True,
        )


def setup(bot: commands.Bot):
    bot.add_cog(ModUtils(bot))
    bot.add_cog(ModUtilsSlash(bot))

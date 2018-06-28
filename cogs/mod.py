"""
    MAT's Bot: An open-source, general purpose Discord bot written in Python.
    Copyright (C) 2018  NinjaSnail1080  (Discord User: @NinjaSnail1080#8581)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mat import mat_color
from discord.ext import commands
import discord
import asyncio

import random


class Moderation:
    "Moderation tools"

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def kick(self, ctx, member, reason=None):
        if ctx.author.permissions_in(ctx.channel).kick_members:
            cant_kick = []
            if reason is None:
                reason = "No reason given"
            for m in ctx.message.mentions:
                if m != self.bot.user:
                    try:
                        await m.kick(reason=reason + " | Action performed by " + ctx.author.name)
                        await ctx.send(embed=discord.Embed(
                            color=mat_color, title=m.name + " kicked by " + 
                            ctx.author.name, description="Reason: " + reason))
                    except discord.Forbidden:
                        cant_kick.append(m.name)
            for i in cant_kick:
                await ctx.send(
                    "I don't have permissions to kick **" + i + "**. What's the point of having "
                    "all these moderation commmands if I can't use them?\nEither I don't have "
                    "perms to kick, period, or my role is too low. Can one of you guys in charge "
                    "fix that please?")
        else:
            await ctx.send(
                "You don't have permissions to kick members. You better take this issue to "
                "whoever's in charge of this server")

    @commands.command()
    @commands.guild_only()
    async def randomkick(self, ctx, members=None):
        if ctx.author.permissions_in(ctx.channel).kick_members:
            rip_list = ["rip", "RIP", "Rip in spaghetti, never forgetti", "RIPeroni pepperoni", 
                        "RIP in pieces", "Rest in pieces"]
            cant_kick = ("Damn, it looks like I don't have permission to kick this person. Could "
                         "one of you guys check my role to make sure I have either the Kick "
                         "Members privilege or the Administrator privilege?\n\nIf I already, do, "
                         "then I probably picked someone with a role higher than mine. So try "
                         "again, or better yet, put my role above everyone else's. Then we can "
                         "make this *really* interesting...")
            if members is None:
                member = random.choice(ctx.channel.guild.members)
                try:
                    await member.kick(
                        reason="Unlucky individual selected by the randomkick performed by " + 
                        ctx.author.name)
                    temp = await ctx.send("And the unlucky individual about to be kicked is...")
                    with ctx.channel.typing():
                        await asyncio.sleep(2)
                        await temp.delete()
                        await ctx.send(embed=discord.Embed(
                            color=mat_color, title=member.name + "!!!", description=random.choice(
                                rip_list)))
                    await ctx.send(
                        "Now someone's gonna have to go invite them back. I suggest you go, " +
                        ctx.author.mention)
                except discord.Forbidden:
                    await ctx.send(cant_kick)
            else:
                member_s = []
                for m in ctx.message.mentions:
                    if m != self.bot.user:
                        member_s.append(m)
                member = random.choice(member_s)
                try:
                    await member.kick(
                        reason="Unlucky individual selected by the randomkick performed by " +
                        ctx.author.name)
                    temp = await ctx.send("And the unlucky individual about to be kicked is...")
                    with ctx.channel.typing():
                        await asyncio.sleep(2)
                        await temp.delete()
                        await ctx.send(embed=discord.Embed(
                            color=mat_color, title=member.name + "!!!", description=random.choice(
                                rip_list)))
                    await ctx.send(
                        "Now someone's gonna have to go invite them back. I suggest you go, " +
                        ctx.author.mention)
                except discord.Forbidden:
                    await ctx.send(cant_kick)
        else:
            await ctx.send(
                "You don't have permissions to kick members. You better take this issue to "
                "whoever's in charge of this server")


def setup(bot):
    bot.add_cog(Moderation(bot))
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

from discord.ext import commands
import discord


class Error_Handlers:
    """Error Handlers for commands"""

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, exception):
        exc = exception
        if isinstance(exc, discord.NotFound):
            return
        if isinstance(exc, commands.BadArgument):
            await ctx.send(ctx.command.brief)
            return
        if isinstance(exc, commands.MissingRequiredArgument):
            return
        else:
            return


def setup(bot):
    bot.add_cog(Error_Handlers(bot))

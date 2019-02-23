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

try:
    from mat_experimental import find_color, delete_message, get_reddit
except ImportError:
    from mat import find_color, delete_message, get_reddit

from discord.ext import commands
from bs4 import BeautifulSoup
from PIL import Image
from zalgo_text.zalgo import zalgo
import discord
import aiohttp
import validators

import random
import datetime
import asyncio
import os
import io
import functools
import string
import typing

import config

#* MAT's Bot uses the NekoBot API for many of these commands.
#* More info at https://docs.nekobot.xyz/

#TODO: Add some more commands and make `thanos` unhidden


class Fun:
    """Fun stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    async def send_nekobot_image(self, ctx, resp):
        if not resp["success"]:
            await ctx.send("Huh, something went wrong. I wasn't able to get the image. Try "
                           "again later", delete_after=5.0)
            return await delete_message(ctx, 5)

        await ctx.send(
            embed=discord.Embed(color=find_color(ctx)).set_image(url=resp["message"]))

    @commands.command(aliases=["randface", "randomface"])
    async def aiface(self, ctx):
        """Gets a picture of a randomly generated face from [thispersondoesnotexist.com](https://thispersondoesnotexist.com/)
        __How it works__: This website uses an AI to generate a picture of a realistic human face, so believe it or not, the people you see when you use this command don't actually exist in real life.
        """
        def save_image(read):
            img = Image.open(io.BytesIO(read))
            img.save(f"aiface.png")

        try:
            with ctx.channel.typing():
                async with self.session.get("https://thispersondoesnotexist.com/image") as w:
                    resp = await w.read()
                await self.bot.loop.run_in_executor(None, functools.partial(save_image, resp))

                embed = discord.Embed(description="Courtesy of [thispersondoesnotexist.com]"
                                      "(https://thispersondoesnotexist.com/)",
                                      color=find_color(ctx))
                await ctx.send("The below image was generated by an AI. It is NOT a picture of "
                               "a real person's face",
                               embed=embed, file=discord.File("aiface.png"))
        except:
            await ctx.send(
                "Hmm, something went wrong and I wasn't able to get an image. Try again later",
                delete_after=5.0)
            return await delete_message(ctx, 5)
        os.remove("aiface.png")

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                      "this: `<prefix> bigletter <text>`", aliases=["bigletters"])
    async def bigletter(self, ctx, *, text: str):
        """Turn text into :regional_indicator_b: :regional_indicator_i: :regional_indicator_g:   :regional_indicator_l: :regional_indicator_e: :regional_indicator_t: :regional_indicator_t: :regional_indicator_e: :regional_indicator_r: :regional_indicator_s:
        Format like this: `<prefix> bigletter <text>`
        """
        try:
            await ctx.channel.trigger_typing()
            text = list(text.lower())
            bigletters = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱',
                          '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽',
                          '🇾', '🇿']
            big = []

            for i in text:
                try:
                    pos = string.ascii_lowercase.index(i)
                    i = bigletters[pos] + " "
                except:
                    if i == " ":
                        i = "  "
                big.append(i)

            await ctx.send("".join(big))
        except:
            await ctx.send("Huh, something went wrong. Try again", delete_after=5.0)
            return await delete_message(ctx, 5)

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                      "this: `<prefix> captcha (OPTIONAL)<@mention user>`")
    async def captcha(self, ctx, user: discord.Member=None):
        """Turns a user's avatar into a CAPTCHA "I am not a robot" test
        Format like this: `<prefix> captcha (OPTIONAL)<@mention user>`
        """
        await ctx.channel.trigger_typing()
        if user is None:
            user = ctx.author
        img = user.avatar_url_as(format="png")
        async with self.session.get(
            f"https://nekobot.xyz/api/imagegen?type=captcha&url={img}"
            f"&username={user.display_name}") as w:
            resp = await w.json()
            await self.send_nekobot_image(ctx, resp)

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                      "this: `<prefix> changemymind <text>`")
    async def changemymind(self, ctx, *, text: str):
        """Dare people to change your mind
        Format like this: `<prefix> changemymind <text>`
        """
        await ctx.channel.trigger_typing()
        async with self.session.get(
            f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}") as w:
            resp = await w.json()
            await self.send_nekobot_image(ctx, resp)

    @commands.command(aliases=["clydify"], brief="You didn't format the command correctly. It's "
                      "supposed to look like this: `<prefix> clyde <text>`")
    async def clyde(self, ctx, *, text: str):
        """Make Clyde say something
        Format like this: `<prefix> clyde <text>`
        """
        await ctx.channel.trigger_typing()
        async with self.session.get(
            f"https://nekobot.xyz/api/imagegen?type=clyde&text={text}") as w:
            resp = await w.json()
            await self.send_nekobot_image(ctx, resp)

    @commands.command()
    async def coinflip(self, ctx):
        """Flips a coin, pretty self-explanatory"""

        coin = random.choice(["Heads!", "Tails!"])
        temp = await ctx.send("Flipping...")
        with ctx.channel.typing():
            await asyncio.sleep(1)
            await temp.delete()
            await ctx.send(coin)

    @commands.command(aliases=["shitpost"])
    async def copypasta(self, ctx):
        """Posts a random copypasta
        Note: For best results, use in a NSFW channel. Then I'll also be able to send NSFW copypastas
        """
        await ctx.channel.trigger_typing()
        return await get_reddit(ctx, self.bot.loop, 1, False, "a copypasta", "copypasta")

    @commands.command(aliases=["zalgo", "zalgofy"],
                      brief="You need to include some text for me to creepify")
    async def creepify(self, ctx, *, text: str):
        """Turns text into c̛̜̎ṟ͆̃e̲͛̋e͇̭̐p̮̺ͮy̷ͪ͡ ź͉ͯą͗ͪl̬̦̈g̯̪̊ờ͙ ṯ̸̦e͔̎̀x̡͈ͪṫ͟͞
        Note: Due to an issue with Discord, this command won't work very well on large amounts of text. Use [this generator](https://lingojam.com/ZalgoText) if you want to convert a lot of text
        """
        await ctx.channel.trigger_typing()
        creepified = zalgo().zalgofy(text)
        if len(creepified) > 2000:
            await ctx.send("Sorry, but the creepified text has too many characters for me to "
                           "send here. Try again with less text", delete_after=5.0)
            return await delete_message(ctx, 5)
        else:
            await ctx.send(creepified)

    @commands.command(aliases=["ch", "cyha", "c&h"])
    async def cyhap(self, ctx):
        """Posts a random Cyanide & Happiness comic"""

        try:
            with ctx.channel.typing():
                async with self.session.get("http://explosm.net/comics/random") as w:
                    soup = BeautifulSoup(await w.text(), "lxml")

                    url = str(w.url)
                    number = url.replace("http://explosm.net/comics/", "")[:-1]
                    image = "http:" + soup.find("img", id="main-comic")["src"]
                    info = soup.find("div", id="comic-author").get_text()

                    embed = discord.Embed(
                        title=f"Cyanide and Happiness #{number}", url=url, color=find_color(ctx))
                    embed.set_author(name="Explosm", url="http://explosm.net/")
                    embed.set_image(url=image)
                    embed.set_footer(text=info)

                    await ctx.send(embed=embed)
        except:
            await ctx.send("Huh, something went wrong. It looks like servers are down so I wasn't"
                           " able to get a comic. Try again in a little bit.", delete_after=6.0)
            return await delete_message(ctx, 6)

    @commands.command(aliases=["ddlcgen"],
                      brief="You didn't format the command correctly. It's supposed to look like "
                      "this: `<prefix> ddlc <character> <background> <pose> <face> <text>`"
                      "\nDo `!mat help ddlc` for more info on how to use this command.")
    async def ddlc(self, ctx, character, background, pose, face, *, text: commands.clean_content(fix_channel_mentions=True)):
        """Generate a DDLC (Doki Doki Literature Club) custom dialogue
        Format like this: `<prefix> ddlc <character> <background> <pose> <face> <text>`
        **Characters**: "sayori", "yuri", "natsuki", OR "monika"
        **Backgrounds**: "bedroom", "class", "closet", "club", "corridor", "house", "kitchen", "residential", OR "sayori_bedroom"
        See the following links to view the **poses** for [Sayori](https://imgur.com/a/qHzyX2w), [Yuri](https://imgur.com/a/tJ72NmL), [Natsuki](https://imgur.com/a/hk2xSfa), and [Monika](https://imgur.com/a/gHE2spo)
        See the following links to view the **faces** for [Sayori](https://imgur.com/a/AD0WjfI), [Yuri](https://imgur.com/a/TtIv3x9), [Natsuki](https://imgur.com/a/Gl6aZSd), and [Monika](https://imgur.com/a/Akc9xtB)
        Text must be less than 140 characters
        """
        characters = ["sayori", "yuri", "natsuki", "monika"]
        backgrounds = ["bedroom", "class", "closet", "club", "corridor", "house", "kitchen",
                       "residential", "sayori_bedroom"]
        monika_faces = [i for i in "abcdefghijklmnopqr"]
        natsuki_faces = [i for i in "abcdefghijklmnopqrstuvwxyz"]
        natsuki_faces.extend(
            ["1t", "2bt", "2bta", "2btb", "2btc", "2btd", "2bte", "2btf", "2btg", "2bth",
            "2bti", "2t", "2ta", "2tb", "2tc", "2td", "2te", "2tf", "2tg", "2th", "2ti"])
        sayori_faces = [i for i in "abcdefghijklmnopqrstuvwxy"]
        yuri_faces = [i for i in "abcdefghijklmnopqrstuvwx"]
        yuri_faces.extend(["y1", "y2", "y3", "y4", "y5", "y6", "y7"])
        ddlc_items = {
            "pose": {
                "monika": [ "1", "2" ],
                "natsuki": [ "1b", "1", "2b", "2"],
                "yuri": ["1b", "1", "2b", "2"],
                "sayori": ["1b", "1", "2b", "2"]
            },
            "face": {
                "monika": monika_faces,
                "natsuki": natsuki_faces,
                "yuri": yuri_faces,
                "sayori": sayori_faces
            }
        }
        reference_links = {
            "pose": {
                "sayori": "https://imgur.com/a/qHzyX2w",
                "yuri": "https://imgur.com/a/tJ72NmL",
                "natsuki": "https://imgur.com/a/hk2xSfa",
                "monika": "https://imgur.com/a/gHE2spo"
            },
            "face": {
                "sayori": "https://imgur.com/a/AD0WjfI",
                "yuri": "https://imgur.com/a/TtIv3x9",
                "natsuki": "https://imgur.com/a/Gl6aZSd",
                "monika": "https://imgur.com/a/Akc9xtB"
            }
        }
        if len(text) >= 140:
            await ctx.send("Text is too long. Must be under 140 characters", delete_after=5.0)
            return await delete_message(ctx, 5)
        character = character.lower()
        if character not in characters:
            await ctx.send(
                "Not a valid character. Must be either `sayori`, `yuri`, `natsuki`, OR `monika`",
                delete_after=7.0)
            return await delete_message(ctx, 7)
        background = background.lower()
        if background not in backgrounds:
            await ctx.send("Not a valid background. Must be either `bedroom`, `class`, `closet`, "
                           "`club`, `corridor`, `house`, `kitchen`, `residential`, OR "
                           "`sayori_bedroom`", delete_after=10.0)
            return await delete_message(ctx, 10)

        if not pose in ddlc_items.get("pose").get(character):
            await ctx.send(
                f"Not a valid pose for {character.capitalize()}. See "
                f"{reference_links.get('pose').get(character)} to view her various poses",
                delete_after=15.0)
            return await delete_message(ctx, 15)
        if not face in ddlc_items.get("face").get(character):
            await ctx.send(
                f"Not a valid face for {character.capitalize()}. See "
                f"{reference_links.get('face').get(character)} to view her various faces",
                delete_after=15.0)
            return await delete_message(ctx, 15)

        await ctx.channel.trigger_typing()
        async with self.session.get("https://nekobot.xyz/api/imagegen?type=ddlc"
                                    f"&character={character}"
                                    f"&background={background}"
                                    f"&body={pose}"
                                    f"&face={face}"
                                    f"&text={text}") as w:
            resp = await w.json()
        await self.send_nekobot_image(ctx, resp)

    @commands.command(brief="The number of sides must be an **integer above 2**. Try again.")
    async def diceroll(self, ctx, sides: int=6):
        """Rolls a dice. By default a 6-sided one though the number of sides can be specified.
        Format like this: `<prefix> diceroll (OPTIONAL)<# of sides>`
        """
        if sides <= 2:
            await ctx.send("The number of sides must be an **integer above 2**. Try again.",
                           delete_after=5.0)
            return await delete_message(ctx, 5)

        dice = str(random.randint(1, sides))
        temp = await ctx.send(f"Rolling a {sides}-sided dice...")
        with ctx.channel.typing():
            await asyncio.sleep(1.5)
            await temp.delete()
            await ctx.send(dice + "!")

    @commands.command()
    async def f(self, ctx):
        """Pay your respects"""

        msg = await ctx.send(
            f"{ctx.author.mention} has paid their respects :heart:. Press F to pay yours.")
        await msg.add_reaction("\U0001f1eb")

    @commands.command()
    async def joke(self, ctx):
        """Sends a joke
        Note: For best results, use in a NSFW channel. Then I'll also be able to send NSFW jokes
        """
        await ctx.channel.trigger_typing()
        return await get_reddit(ctx, self.bot.loop, 1, False, "a joke", "jokes")

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                      "this: `<prefix> phcomment (OPTIONAL)<@mention user> <comment>`")
    async def phcomment(self, ctx, user: typing.Optional[discord.Member]=None, *, comment: str):
        """Generate a PornHub comment!
        Format like this: `<prefix> phcomment (OPTIONAL)<@mention user> <comment>`
        """
        await ctx.channel.trigger_typing()
        if user is None:
            user = ctx.author
        pfp = user.avatar_url_as(format="png")
        async with self.session.get("https://nekobot.xyz/api/imagegen?type=phcomment"
                                    f"&image={pfp}&text={comment}"
                                    f"&username={user.display_name}") as w:
            resp = await w.json()
            await self.send_nekobot_image(ctx, resp)

    @commands.command()
    async def lenny(self, ctx):
        """A list of Lenny faces for all your copypasting needs"""

        embed = discord.Embed(
            title="A list of Lenny faces for all your copypasting needs",
            color=find_color(ctx), url="https://www.lennyfaces.net/")

        embed.add_field(name="Classic", value="( ͡° ͜ʖ ͡°)")
        embed.add_field(name="Pissed Off", value="( ͠° ͟ʖ ͡°)")
        embed.add_field(name="Winky", value="( ͡~ ͜ʖ ͡°)")
        embed.add_field(name="Wide-Eyed", value="( ͡◉ ͜ʖ ͡◉)")
        embed.add_field(name="Wide-Eyed 2", value="( ͡☉ ͜ʖ ͡☉)")
        embed.add_field(name="Happy", value="( ͡ᵔ ͜ʖ ͡ᵔ )")
        embed.add_field(name="Sad", value="( ͡° ʖ̯ ͡°)")
        embed.add_field(name="With Ears", value="ʕ ͡° ͜ʖ ͡°ʔ")
        embed.add_field(name="Communist", value="(☭ ͜ʖ ☭)")
        embed.set_footer(text="From: https://www.lennyfaces.net/")

        await ctx.send(embed=embed)

    @commands.command()
    async def meirl(self, ctx):
        """Sends posts that are u irl"""

        await ctx.channel.trigger_typing()
        return await get_reddit(
            ctx, self.bot.loop, 1, False, "a meme", "me_irl", "me_irl", "meirl")

    @commands.command()
    async def meme(self, ctx):
        """Posts a dank meme"""

        await ctx.channel.trigger_typing()
        return await get_reddit(
            ctx, self.bot.loop, 1, False, "a meme", "memes", "dankmemes", "dankmemes")

    @commands.command(aliases=["weirdspeak"])
    async def mock(self, ctx, *, stuff: str=None):
        """Say something and I'll mock you"""

        if stuff is None:
            await ctx.send("Dude, you need to say something for me to mock", delete_after=5.0)
            return await delete_message(ctx, 5)

        await ctx.channel.trigger_typing()

        embed = discord.Embed(color=find_color(ctx))
        embed.set_image(url="https://i.imgur.com/8NmOT8w.jpg")
        stuff = list(stuff.lower())
        mock = []
        for i in stuff:
            if i == "c":
                if random.randint(1, 2) == 1:
                    i = "k"
            elif i == "x":
                if random.randint(1, 2) == 1:
                    i = "ks"
            if random.randint(1, 2) == 1:
                i = i.upper()
            mock.append(i)

        await ctx.send(content="".join(mock), embed=embed)

    @commands.command(brief="You're supposed to include a subreddit for me to get a random post "
                      "from after the command. Like this: `<prefix> reddit <subreddit>`")
    async def reddit(self, ctx, sub):
        """Get a random post from any subreddit
        Format like this: `<prefix> reddit <subreddit>`
        Notes: Capitalization doesn't matter when typing the name of the sub
        """
        await ctx.channel.trigger_typing()
        return await get_reddit(ctx, self.bot.loop, 2, True, "a post from this sub", sub)

    @commands.command()
    async def reverse(self, ctx, *, stuff: str=None):
        """Reverse the text you give me!"""

        if stuff is None:
            await ctx.send("Dude, you need to give me some text to reverse", delete_after=5.0)
            return await delete_message(ctx, 5)

        else:
            stuff = stuff[::-1]
            stuff = stuff.replace("@everyone", "@\u200beveryone")
            stuff = stuff.replace("@here", "@\u200bhere")

            await ctx.send(stuff)

    @commands.command(aliases=["print", "printf", "System.out.println", "echo", "std::cout<<",
                               "puts"])
    async def say(self, ctx, *, stuff: str=None):
        """Make me say something!"""

        if stuff is None:
            await ctx.send("Dude, you need to give me something to say", delete_after=5.0)
            return await delete_message(ctx, 5)

        else:
            stuff = stuff.replace("@everyone", "@\u200beveryone")
            stuff = stuff.replace("@here", "@\u200bhere")

            await ctx.send(stuff)

    @commands.command(aliases=["showerthoughts"])
    async def showerthought(self, ctx):
        """Posts a random showerthought"""

        await ctx.channel.trigger_typing()
        return await get_reddit(ctx, self.bot.loop, 1, False, "a showerthought", "showerthoughts")

    @commands.command(hidden=True)
    async def thanos(self, ctx):
        """Thanos did nothing wrong"""

        await ctx.channel.trigger_typing()
        return await get_reddit(
            ctx, self.bot.loop, 1, False, "a thanos meme", "thanosdidnothingwrong")

    @commands.command(brief="You didn't format the command correctly. You're supposed to "
                      "include some text for me to thiccify")
    async def thiccify(self, ctx, *, text):
        """Turns text into 乇乂丅尺卂 丅卄工匚匚 letters
        Format like this: `<prefix> thiccify <text>`
        """
        try:
            await ctx.channel.trigger_typing()
            text = list(text.lower())
            thicc_letters = "卂乃匚刀乇下厶卄工丁长乚从𠘨口尸㔿尺丂丅凵リ山乂丫乙"
            thicc = []

            for i in text:
                try:
                    pos = string.ascii_lowercase.index(i)
                    i = thicc_letters[pos]
                except:
                    if i == " ":
                        i = "  "
                thicc.append(i)

            await ctx.send("".join(thicc))
        except:
            await ctx.send("Huh, something went wrong. Try again", delete_after=5.0)
            return await delete_message(ctx, 5)

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                      "this: `<prefix> trap <@mention user>`")
    async def trap(self, ctx, member: discord.Member):
        """Trap another user with your trapcard!
        Format like this: `<prefix> trap <@mention user>`
        """
        await ctx.channel.trigger_typing()
        async with self.session.get(
            f"https://nekobot.xyz/api/imagegen?type=trap&name={member.display_name}"
            f"&author={ctx.author.display_name}&image={member.avatar_url_as(format='png')}") as w:
            resp = await w.json()
            await self.send_nekobot_image(ctx, resp)

    @commands.command(brief="You didn't format the command correctly. You're supposed to include "
                      "some text for the tweet `<prefix> trumptweet <tweet>`")
    async def trumptweet(self, ctx, *, tweet: str):
        """Tweet as Trump!
        Format like this: `<prefix> trumptweet <tweet>`
        """
        await ctx.channel.trigger_typing()
        async with self.session.get(
            f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={tweet}") as w:
            resp = await w.json()
            await self.send_nekobot_image(ctx, resp)

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                      "this: `<prefix> tweet <twitter usernamer> <tweet>`")
    async def tweet(self, ctx, user: str, *, tweet: str):
        """Tweet as yourself or another twitter user!
        Format like this: `<prefix> tweet <twitter username> <tweet>`
        """
        await ctx.channel.trigger_typing()
        async with self.session.get("https://nekobot.xyz/api/imagegen?type=tweet"
                                    f"&username={user}&text={tweet}") as w:
            resp = await w.json()
            await self.send_nekobot_image(ctx, resp)

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                      "this: `<prefix> whowouldwin <@mention user 1> (OPTIONAL)<@mention user 2>`")
    async def whowouldwin(self, ctx, user1: discord.Member, user2: discord.Member=None):
        """Who would win?
        Format like this: `<prefix> whowouldwin <@mention user 1> (OPTIONAL)<@mention user 2>`
        """
        await ctx.channel.trigger_typing()
        if user2 is None:
            user2 = ctx.author
        img1 = user1.avatar_url_as(format="png")
        img2 = user2.avatar_url_as(format="png")
        async with self.session.get("https://nekobot.xyz/api/imagegen?type=whowouldwin"
                                    f"&user1={img1}&user2={img2}") as w:
            resp = await w.json()
            await self.send_nekobot_image(ctx, resp)

    @commands.command()
    async def xkcd(self, ctx):
        """Posts a random xkcd comic"""
        try:
            with ctx.channel.typing():
                async with self.session.get("https://c.xkcd.com/random/comic/") as w:
                    soup = BeautifulSoup(await w.text(), "lxml")

                    url = str(w.url)
                    number = url.replace("https://xkcd.com/", "")[:-1]
                    title = soup.find("div", id="ctitle").get_text()
                    comic = soup.find("div", id="comic")
                    image = "https:" + comic.img["src"]
                    caption = comic.img["title"]

            embed = discord.Embed(
                title=f"{title} | #{number}", color=find_color(ctx), url=url)

            embed.set_author(name="xkcd", url="https://xkcd.com/")
            embed.set_image(url=image)
            embed.set_footer(text=caption)

            await ctx.send(embed=embed)
        except:
            await ctx.send("Huh, something went wrong. It looks like servers are down so I wasn't"
                           " able to get a comic. Try again in a little bit.", delete_after=6.0)
            return await delete_message(ctx, 6)


def setup(bot):
    bot.add_cog(Fun(bot))

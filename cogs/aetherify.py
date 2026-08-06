import asyncio
import random

from disnake.ext import commands
from disnake.ext.commands.params import Param
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot

AETHER_LETTERS = ["π", "§", "ů", "ö", "🗣️", "ǚ", "ǘ", "ǜ", "ů̈́"]


class Aetherify(V2BotCog):
    @commands.slash_command(name="aetherify", description="instant aethering")
    async def aetherify_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        msg: str = Param(desc="the text to aetherify"),
    ):
        await inter.response.defer()

        aethered = await asyncio.to_thread(self.aetherify, msg)

        await inter.edit_original_response(aethered)

    @commands.slash_command(name="unaetherify", description="instant unaethering")
    async def unaetherify_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        msg: str = Param(desc="the text to unaetherify"),
    ):
        await inter.response.defer()

        unaethered = await asyncio.to_thread(self.unaetherify, msg)

        await inter.edit_original_response(unaethered)

    @staticmethod
    def aetherify(text: str) -> str:
        aethered = ""
        for letter in text:
            code = ord(letter) - 0x10
            if code == 0x10:
                aethered += " "
            elif code < 0x20:
                aethered += random.choice(AETHER_LETTERS)
            else:
                aethered += chr(code)

        return aethered

    @staticmethod
    def unaetherify(text: str) -> str:
        unaethered = ""
        for letter in text:
            code = ord(letter) + 0x10
            if code == 0x20:
                unaethered += " "
            else:
                unaethered += chr(code)

        unaethered = unaethered.replace("hio", "help")
        unaethered = unaethered.replace("HIO", "HELP")

        unaethered = unaethered.replace("hue", "help (said evilishly)")
        unaethered = unaethered.replace("HUE", "HELP (said evilishly)")

        return unaethered


def setup(bot: V2Bot):
    bot.add_cog(Aetherify(bot))

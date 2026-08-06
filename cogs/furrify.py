import asyncio
from pydoc import replace
import random

from disnake.ext import commands
from disnake.ext.commands.params import Param
from disnake.interactions import ApplicationCommandInteraction

from cogs.v2cog import V2BotCog
from main import V2Bot

REPLACE_RULES: dict[str, str] = {"r": "w", "l": "w", "sp": "spw", "te": "twe"}

ADDITIONS: list[list[str]] = [
    [
        "\\*yip\\*",
        "\\*yiiip\\*" "\\*meow\\*",
        "\\*mrreow\\*",
        "\\*mrrr\\*",
        "\\*purr*\\*",
    ],
    [
        ":3",
        ":3",
        ">:3",
        ">:3c",
        "OwO",
        "owo",
        "UwU",
        "qwq",
        "TwT",
        "o//w//o",
        ">w<",
        ">//w//<",
        ">m<" ">//m//<",
        "3:",
        "3:<",
        ":з",
        ">:з",
    ],
]


class FurrifySlashCommand(V2BotCog):
    @commands.slash_command(
        name="furrify",
        description="makes you spweak much bettew, yip! :3 *cute tailwag* >w<",
    )
    async def furrify_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        text: str = Param(desc="the text to fuwwify :3"),
    ):
        await inter.response.defer(ephemeral=True)

        furrified_text = await asyncio.to_thread(self.furrify_text, text)

        await inter.edit_original_response(furrified_text)

    @staticmethod
    def furrify_text(text: str) -> str:
        for pattern in REPLACE_RULES:
            text = text.replace(pattern, REPLACE_RULES[pattern])

        for x in range(len(ADDITIONS)):
            text += f" {random.choice(ADDITIONS[x])}"

        return text


def setup(bot: V2Bot):
    bot.add_cog(FurrifySlashCommand(bot))

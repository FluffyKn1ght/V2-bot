import os
import random

from disnake.abc import Messageable
from disnake.ext import commands
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.params import Param
from disnake.file import File
from disnake.interactions import ApplicationCommandInteraction
from disnake.member import Member
from disnake.message import Message

from cogs.v2cog import V2BotCog
from main import V2Bot


class Bully(V2BotCog):
    def __init__(self, bot: V2Bot) -> None:
        super().__init__(bot)

        self.bully_types = []

    @Cog.listener("on_ready")
    async def on_ready(self):
        self.reload_bully_types()

    def reload_bully_types(self):
        self.bully_types = [x for x in self.bot.config["bully"]]

    async def bully(
        self, dirname: str, channel: Messageable, reply_to: Message | None = None
    ):
        files = []

        for file in os.listdir(f"./medihha/{dirname}"):
            fullpath = os.path.join(f"./medihha/{dirname}", file)
            if os.path.isfile(fullpath):
                files.append(fullpath)

        if reply_to:
            await channel.send(
                ":3", file=File(random.choice(files)), reference=reply_to
            )
        else:
            await channel.send(":3", file=File(random.choice(files)))

    async def bully_slashcmd_autocomp(
        self, inter: ApplicationCommandInteraction, user_input: str
    ):
        return self.bully_types

    @commands.slash_command(
        name="bully",
        description="ur a gay furry ur a gay furry ur a gay furry ur a gay furry ur a gay furry ur a gay furry ur a gay furry ur a gay furry"[
            :100
        ],
    )
    async def bully_slash_command(
        self,
        inter: ApplicationCommandInteraction,
        bully_type: str = Param(
            desc="how to bully the user", autocomp=bully_slashcmd_autocomp
        ),
    ):
        await inter.response.defer(ephemeral=True)

        try:
            await self.bully(
                self.bot.config["bully"][bully_type]["dirname"],
                inter.channel,
                (
                    await inter.channel.fetch_message(
                        self.bot.selected_messages[inter.user.id]
                    )
                    if inter.user.id in self.bot.selected_messages
                    else None
                ),
            )
        except KeyError:
            await inter.edit_original_response(
                "what the fuck is that bully type vro :wilted_rose:"
            )
            return

        await inter.edit_original_response("psychological warfare unleashed :+1:")


def setup(bot: V2Bot):
    bot.add_cog(Bully(bot))
